import logging


logger = logging.getLogger(__name__)


class IHandler:
    def handle(self, *args, **kwargs) -> bool:
        """
        :param args: 
        :param kwargs: 
        :return:
            True если эвент был обработан в данном методе, False в противном случае.
            Это означает что эвент пойдет дальше по ветке к родительскому узлу
        """
        logger.debug(f">>> {self.__class__.__name__}.handle(*{args}, **{kwargs})")
        return False
