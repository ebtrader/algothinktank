import time
import random
import pandas as pd
import time

# create a list and then append the list with the output of the variables
# https://www.delftstack.com/howto/python/append-multiple-elements-python/

SLEEP_SECONDS = 3
TICKS_IN_TEST_PERIOD = 100

class RandomNumbersInLists:

    def __init__(self):
        self.stock_px1 = 0
        self.stock_px2 = 0
        self.stock_px3 = 0
        self.sample_list = []
        self.df = pd.DataFrame(columns=['prices'])
        self.tick_count = 0
        self.sleep_seconds = SLEEP_SECONDS
        self.ticks_in_test_period = TICKS_IN_TEST_PERIOD
        self.random_list = []
        self.column_converted_to_list = []
        self.dict_test = {}

    def generate_random_stock_px(self):
        self.random_list = random.sample(range(0,100), 7)
        print(self.random_list)

    def generate_stock_px(self):
        self.stock_px1 = random.randint(3,10)
        # print(self.stock_px1)
        self.stock_px2 = random.randint(3, 10)
        # print(self.stock_px2)
        self.stock_px3 = random.randint(3, 10)
        # print(self.stock_px3)

    def create_list(self):
        self.sample_list.append(self.stock_px1)
        self.sample_list.append(self.stock_px2)
        self.sample_list.append(self.stock_px3)
        # print(self.sample_list)

    def create_list1(self):
        self.sample_list = [self.stock_px1, self.stock_px2, self.stock_px3]
        # print(self.sample_list)

    def create_df(self):
        self.df = pd.DataFrame(self.sample_list, columns=['prices'])
        # print(self.df)

    def reset_index(self):
        self.df.reset_index(inplace=True)
        self.df = self.df.rename(columns={'index': 'new_index'})

    def df_add_columns(self):
        self.df['add'] = self.df['prices'] + 3
        print(self.df)

    def column_to_list(self):
        self.column_converted_to_list = self.df['add'].tolist()
        # print(self.column_converted_to_list)

    def columns_to_dict(self):
        self.dict_test = self.df.set_index('new_index').to_dict()['add']
        print(self.dict_test)

    def playlist(self):
        while self.tick_count < self.ticks_in_test_period:
            self.generate_stock_px()
            self.create_list1()
            self.create_df()
            self.reset_index()
            self.df_add_columns()
            self.column_to_list()
            self.columns_to_dict()
            time.sleep(self.sleep_seconds)
            self.tick_count += 1

def main():
    app = RandomNumbersInLists()
    app.playlist()

if __name__ == "__main__":
    main()
