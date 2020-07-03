import matplotlib.pyplot as plt

class graphic:
    def __init__(self):
        self.fig,self.axis=plt.subplots(nrows=1,ncols=1)

    def render(self,data,title,label,xlabel,ylabel):
        self.axis[0,0].plot(data[0],data[1],label=label)
        self.axis[0,0].set_title(title)
        self.axis[0,0].set_xlabel(xlabel)
        self.axis[0,0].set_ylabel(ylabel)
