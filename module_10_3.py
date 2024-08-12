import threading
from random import randint
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            amount = randint(50, 500)
            with self.lock:
                if self.balance + amount >= 500 and not self.lock.locked():
                    self.lock.release()
                self.balance += amount
                print(f'Пополнение: {amount}. Баланс: {self.balance}')
            sleep(0.001)

    def take(self):
        for _ in range(100):
            amount = randint(50, 500)
            print(f'Запрос на {amount}')
            with self.lock:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f'Снятие: {amount}. Баланс: {self.balance}')
                else:
                    print("Запрос отклонён, недостаточно средств")
                    self.lock.acquire()
                    break

if __name__ == "__main__":
    bk = Bank()

    th1 = threading.Thread(target=Bank.deposit, args=(bk,), name="DepositThread")
    th2 = threading.Thread(target=Bank.take, args=(bk,), name="TakeThread")

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    print(f'Итоговый баланс: {bk.balance}')