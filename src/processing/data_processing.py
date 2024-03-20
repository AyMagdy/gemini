import connection.socket_connection as sockcon
import utilities.utilities as utilities
from processing import utils
import json
import ssl
import queue
import pandas as pd
from threading import Lock
import threading
import logging


logger = logging.getLogger('info_logger')

#Ouster detect defined variables
ENDIAN_TYPE = "big"
FRAME_SIZE_B = 4
QUEUE_MAX_SIZE = 10
TIMESTAMP = {}


# Writes the received data from the stream to a queue
def put_object_to_queue(data_queue: queue.Queue, ssl_socket_client: ssl.SSLSocket,q_ready_event:threading.Event) -> None:
    """ Description:
            read data from stream and put in queue this function doesn't end until queue is full
            or there is not data recieved from the stream (byte array is empty).
        
        Args:
            socket connection with ssl wrap.
            data_queue to put received data in.
        Returns:
            None.
    """
    
    while True:
        if (data_queue.qsize() < data_queue.maxsize ):
            # logger.info("reading from tcp putting in queue queue size is %d",queue.qsize())
            frame_size_b = utilities.recv_stream(ssl_socket_client, FRAME_SIZE_B)
            if len(frame_size_b) == 0:
                logger.info(f'error recieved frame size bytearray {len(frame_size_b)}')
                break
            frame_size = int.from_bytes(frame_size_b, byteorder=ENDIAN_TYPE)
            data = utilities.recv_stream(ssl_socket_client, frame_size)
            if len(data) == 0:
                logger.info(f'error recieved data length {len(data)}')
                break
            data = json.loads(data.decode("utf-8"))
            data_queue.put(data)
            logger.info(f'queue size is {data_queue.qsize()}')
            logger.info(f'{threading.enumerate()}')
            if(data_queue.qsize() == 1):
                q_ready_event.set()
                logger.info('queue is ready')
                                
        else:
            logger.info(f'queue size = {data_queue.qsize()} break has occured from {put_object_to_queue.__name__} from module {__name__}')
            break
    logger.info('thread terminated put to queue')



def get_from_queue(data_queue: queue.Queue,lock:Lock,q_ready_event:threading.Event,d_ready_event:threading.Event) -> None:
    """ Description:
            this function checks if the queue is not empty then
            reads the time stamp of the received frame from queue
            time stamp is saved in TIMESTAMP global dictionary as the key
            the values are dictionaries of parameter name as key and values of
            the data values.

        Example:
            {1701174658528965: { 'obj_id': [11111, 22222, 33333, 44444]},'position': [111, 222, 333, 4444]}.
        
        Args:
            queue to get timestamp and other data from 
                              
        Returns:
            None

        Descritpion: //#//
    """

    global TIMESTAMP
    
    temp = {}
    while True:
        logger.info('before waitting for queue')
        q_ready_event.wait()
        logger.info('after waittting for queue')
        try:   # if queue is not empty pop to temp
            temp = data_queue.get()
            logger.debug(f'temp is --------------------------------------------{temp}')
            timestamp_list      = utilities.get_root_info(temp,'timestamp')    # list of all time stamps received 
            logger.debug(f'time stamplist from {__name__} is {timestamp_list}')
            data_queue.task_done()
        except data_queue.empty:
            logger.info('queue is empty no data to read ')
            break

        # iterate on each time stamp and save its objects' data
        for stamp in (timestamp_list):
            index = timestamp_list.index(stamp) 
            # list of the data specified by its name.
            obj_id               = utilities.get_object_list_arr(temp,index,'id')
            creation_time        = utilities.get_object_list_arr(temp,index,'creation_ts')
            frame_count          = utilities.get_object_list_arr(temp,index,'frame_count')
            classification       = utilities.get_object_list_arr(temp,index,'classification') 
            velocity             = utilities.get_object_list_arr(temp,index,'velocity')
            position             = utilities.get_object_list_arr(temp,index,'position')
            heading              = utilities.get_object_list_arr(temp,index,'heading')
            distance_from_sensor = utilities.get_object_list_arr(temp,index,'distance_to_primary_sensor')

            obj = dict([('obj_id',obj_id),('creation_time',creation_time),
                        ('frame_count',frame_count),('classification',classification),
                        ('velocity',velocity),('position',position),('heading',heading),('distance_to_primary_sensor',distance_from_sensor)])
            logger.info('get from queue has taken the LOCK')
            
            with lock:
                logger.info('inside lock block')
                TIMESTAMP.update({str(stamp):obj})
                if (len(TIMESTAMP) == 1):
                    d_ready_event.set()
                    logger.info('TIMESTAMP data is ready')
            logger.info('out side lock')
    logger.info('thread terminated')


# post processing on the data from the global variables          
def processing_from_queue(lock:Lock,d_ready_event:threading.Event)->None:
    """ Description:
            This function is meant to calculate furthur processes after refining the data from stream.
        
        Args:
            lock to protect shared resources
            d_read_event waits for the signal when data is ready to be processed then thread starts.

        Returns:
            None
    """

    global TIMESTAMP

    while True:
        d_ready_event.wait()
        with lock:
            posdf = utils.get_pos_df(TIMESTAMP)
            veldf = utils.get_vel_df(TIMESTAMP)
            # heddf = utils.get_hed_df(TIMESTAMP) 
            disdf = utils.get_dis_from_sensor(TIMESTAMP)
 
        try:
            indicies = list(utils.get_nearest_from_sensor(disdf,str(1)).index)
            # print(utilities.get_velocity_diff(veldf,index1=indicies[0],index2=indicies[1]))
            vel_mag = utils.calc_vel_mag_diff(veldf,0,index1=indicies[0],index2=indicies[1])
            pos_mag = utils.calc_pos_mag_diff(posdf,0,index1=indicies[0],index2=indicies[1])
            time_to_col = utils.time_to_col(vel=vel_mag,pos=pos_mag)
            print(f'Expected Time To Collision is {time_to_col}.')
        except Exception as e:
            logger.info('EXCEPTION OCCURED RESTARTING THE THREAD WILL TAKE PLACE CONSIDER THE ERROR FIRST!!!')
            logger.info(f'{e}')
            threading.Thread(target=processing_from_queue,args=(lock,d_ready_event,))
            

            


if __name__ == '__main__':
    
    logging_format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename='mylogfile.log',filemode='w',format=logging_format, level=logging.INFO,datefmt="%H:%M:%S")
    
    lock = Lock()

    # creat a queue to recieve in it the data from the stream
    my_queue = queue.Queue(QUEUE_MAX_SIZE)
    my_ssl = sockcon.connect_to_ssl_socket()
    
    with my_ssl:
         
        thread1 = threading.Thread(target=put_object_to_queue,args=(my_queue,my_ssl))
        thread2 = threading.Thread(target=get_from_queue,args=(my_queue,lock,))
        thread3 = threading.Thread(target=processing_from_queue,args=(lock,))

        thread1.start()
        thread2.start()
        thread3.start()

        thread2.join()
        thread1.join()
        thread3.join()