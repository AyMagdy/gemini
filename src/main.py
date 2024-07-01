import connection.socket_connection as sockcon
import processing.data_processing as processing 
import threading
import logging
import queue
import time

def main():
    """
        the starting function of the project.
        this function defines two types of loggers to be used in dignosing system healt 
        first logger for information where it loggs the normal operation of the system creation of queue size of queue
        and makes the system more friendly.
        second logger for warnings such as no data present, connection failed and other messages which needs action.
    """
    logging.getLogger().setLevel(logging.INFO)
    info_logger_handler = logging.FileHandler('info_logger.log',mode='w')
    info_logger_handler.setLevel(logging.INFO)
    info_logger_format = logging.Formatter("%(asctime)s :: %(levelname)s :: %(threadName)s :: %(module)s :: %(funcName)s :: %(lineno)d :: %(message)s")
    info_logger_handler.setFormatter(info_logger_format)
    
    warn_logger_handler = logging.FileHandler('warn.log',mode="w")
    warn_logger_handler.setLevel(logging.WARNING)
    
    info_logger = logging.getLogger(name='info_logger')
    info_logger.addHandler(info_logger_handler)
    warn_logger = logging.getLogger(name='warn_logger')
    warn_logger.addHandler(warn_logger_handler)

    # logging.basicConfig(filename='loggingfile.log',filemode='w',format=formatter, level=logging.INFO,datefmt="%d-%m-%Y - %H:%M:%S")
    info_logger.info("hello")
    warn_logger.warning('warn msgg')
    
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
        
