import threading
import random
import time

class CustomLock:
    def __init__(self):
        self.locked = False
    
    def acquire(self):
        while self.locked:
            pass
        self.locked = True
    
    def release(self):
        self.locked = False

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = CustomLock()
        self.deposit_count = 0
        self.take_count = 0
    
    def deposit(self):
        for _ in range(100):  
            amount = random.randint(50, 500)
            self.lock.acquire()
            self.balance += amount
            print(f"Пополнение: {amount}. Баланс: {self.balance}")
            self.lock.release()
            
            if self.balance >= 500:
                print("Баланс достиг 500 или больше, можно продолжать операции.")
            
            time.sleep(0.001)
            self.deposit_count += 1
    
    def take(self):
        for _ in range(100):  
            request_amount = random.randint(50, 500)
            print(f"Запрос на {request_amount}")
            time.sleep(0.001)
            
            if request_amount <= self.balance:
                self.lock.acquire()
                self.balance -= request_amount
                print(f"Снятие: {request_amount}. Баланс: {self.balance}")
                self.lock.release()
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()
                self.lock.release()
            
            self.take_count += 1
    
    def start(self):
        th1 = threading.Thread(target=self.deposit)
        th2 = threading.Thread(target=self.take)
        
        th1.start()
        th2.start()
        
        th1.join()
        th2.join()
        
        print(f'Итоговый баланс: {self.balance}')
        print(f'Количество транзакций пополнения: {self.deposit_count}')
        print(f'Количество транзакций снятия: {self.take_count}')

bank = Bank()
bank.start()
