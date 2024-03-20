import connection.socket_connection as sockcon
import processing.data_processing as processing 
import threading
import logging
import queue
import time

def main():
    """ 
        Brief:
            This main.py file serves as the entry point for a multi-threaded application that

            1) establishes an SSL socket connection, 
            2) receives data from the connection, 
            3) processes the data.

            The application is structured around a producer-consumer pattern using threads and a queue.
            A log is added for future work which will help id diagnosing and monitoring the health of the system.
                                ***REFERE TO LAST SUBTITLE***
    
        Global Constants:
            DATA_QUEUE is a queue created with a maximum size of 5.(size is fo tessting)
            This queue will be used to store data received from the SSL socket connection.

            LOCK is created to ensure thread-safe operations when accessing shared resources.
        
            QUEUE_READY_EVENT and DATA_READY_EVENT, are created to synchronize the start or signal process thread operations.
    
        SSl Socket Conection:
            The connect_to_ssl_socket function from the connection.socket_connection module is called to establish an SSL socket connection.
            This function is defined in socket_connection.py and attempts to create a secure connection using the TLSv1.2 protocol.
            If the connection is successful, an informational message is logged stating that the connection has been established.

        Thread Creatin and Execution:
            Three threads are created for different purposes:
            put_to_queue_thr:    This thread is responsible for READING data from the SSL socket connection and putting it into DATA_QUEUE.It uses the put_object_to_queue function from the processing.data_processing module.
            read_from_queue_thr: This thread is responsible for RETRIEVING data from DATA_QUEUE and making it available for processing.It uses the get_from_queue function from the processing.data_processing module.
            process_thr:         This thread is responsible for PROCESSING the data retrieved from the queue.It uses the processing_from_queue function from the processing.data_processing module.
            The join method is called on each thread to ensure that the main thread waits for their completion before proceeding.

        Description:
            This application is an example for the future work it was made to be generic as possible by using the approch of modularity.
            in this application the time of collision is calculated:
                1) find the nearest two object to the sensor (an information retrieved from the object list recieved from the stream)
                2) find the relative velocity magnitude between the same two objects. (the same time stamp is taken in consideratin to make sure the specific required object is found)
                3) find the relative position magnitude between the same two objects. ()
                4) estimate the time of collision between the objects.
        
        ***ASSUMPTIONS*** is made that both objects are heading towards the sensor. 
        for future work this will be taken in consideration for robust results.
    """
    
    logging.getLogger().setLevel(logging.INFO)
    info_logger_handler = logging.FileHandler('info.log',mode='w')
    info_logger_handler.setLevel(logging.INFO)
    info_logger_format = logging.Formatter("%(asctime)s :: %(levelname)s :: %(threadName)s :: %(module)s :: %(funcName)s :: %(lineno)d :: %(message)s")
    info_logger_handler.setFormatter(info_logger_format)
    
    war_logger_handler = logging.FileHandler('warn.log',mode="w")
    war_logger_handler.setLevel(logging.WARNING)
    
    info_logger = logging.getLogger(name='info_logger')
    info_logger.addHandler(info_logger_handler)
    warn_logger = logging.getLogger(name='warn_logger')
    warn_logger.addHandler(war_logger_handler)

    # logging.basicConfig(filename='loggingfile.log',filemode='w',format=formatter, level=logging.INFO,datefmt="%d-%m-%Y - %H:%M:%S")
    info_logger.info("hello")
    warn_logger.warning('warn msg')
    
    #global constants
    DATA_QUEUE:queue.Queue =  queue.Queue(maxsize = 5) 
    LOCK = threading.Lock() 
    QUEUE_READY_EVENT = threading.Event()
    DATA_READY_EVENT = threading.Event()
    # Creat an ssl wrap socket connection
    ssl_socket_client = sockcon.connect_to_ssl_socket()
           
    if  ssl_socket_client:
        info_logger.info('CONNECTION ESTABLISHED.....')
        time.sleep(2)
        with ssl_socket_client:
        
            # Creat threads
            put_to_queue_thr = threading.Thread(target=processing.put_object_to_queue,args=(DATA_QUEUE,ssl_socket_client,QUEUE_READY_EVENT))
            read_from_queue_thr = threading.Thread(target=processing.get_from_queue,args=(DATA_QUEUE,LOCK,QUEUE_READY_EVENT,DATA_READY_EVENT))
            process_thr = threading.Thread(target=processing.processing_from_queue,args=(LOCK,DATA_READY_EVENT))
            
            # Start threads
            put_to_queue_thr.start()
            read_from_queue_thr.start()
            process_thr.start()
                  
    
            # Wait for threads
            put_to_queue_thr.join()
            read_from_queue_thr.join()
            process_thr.join()
            
    
        
            # end of main thread
            print("end of program")
    else:
        print("no connection ........ check docker")
        




if __name__ == '__main__':
    main()
        
