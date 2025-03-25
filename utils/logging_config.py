import logging

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG, 
        filename='app.log', 
        filemode='w', 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )