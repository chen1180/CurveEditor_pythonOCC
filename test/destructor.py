class test:
    def __init__(self):
        print("created")
    def __del__(self):
        print("delted")
a=test()
del a