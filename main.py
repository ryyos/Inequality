from src import Inequality
from src import logger
from time import perf_counter

if __name__ == '__main__':
    ine = Inequality()
    start = perf_counter()

    logger.info('Scraping started..')
    
    ine.main()

    logger.info('scraping is complete..')
    logger.info(f'total scraping time: {perf_counter() - start}')
