from modulos import *


class MetaIPChecker(ABCMeta):
    def __new__(cls, name, bases, dct):
        if 'get_ip_address' not in dct:
            pass
        return super().__new__(cls, name, bases, dct)


class AbstractIPChecker(ABC, metaclass=MetaIPChecker):
    @abstractmethod
    def get_ip_address(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__} Class"


class IPChecker(AbstractIPChecker):
    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except socket.error as err:
            pass
            return None


class NetworkObserver:
    def __init__(self, ip_checker):
        self.ip_checker = ip_checker

    def check_network(self, desired_ip):
        current_ip = self.ip_checker.get_ip_address()
        if current_ip == desired_ip:
            pass
            AnimatedBanner('Mapeamento de Shapefiles!!', [Fore.LIGHTMAGENTA_EX]).display()
            main()
        else:
            pass


class AbstractLoadingBar(ABC):
    @abstractmethod
    def display(self):
        pass
    

class GreenLoadingBar(AbstractLoadingBar):
    def display(self):
        for i in trange(int(7**7.5), bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)):
            pass
        os.system('cls')
        

class AbstractBanner(ABC):
    @abstractmethod
    def display(self):
        pass
    

class AnimatedBanner(AbstractBanner):
    def __init__(self, text, colors, font='big'):
        self.text = text
        self.colors = colors
        self.custom_fig = Figlet(font=font)

    def display(self):
        for color in self.colors:
            for line in self.custom_fig.renderText(self.text).splitlines():
                print(color + line, flush=True)
                time.sleep(0.05)
        time.sleep(0.5)
        

def app():
    desired_ip = "172.24.66.8"
    checker = IPChecker()
    observer = NetworkObserver(checker)
    observer.check_network(desired_ip)


if __name__ == "__main__":
    app()
