import pathlib
#import numpy as np
import cv2 as cv

class Game:
    
    def __init__(self):

        self.frames = []
        for path in sorted(pathlib.Path('data/frames').glob('*.png')):
            img = cv.imread(str(path))
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            self.frames.append(img)
        self.properties = {'width': 1920,
                           'height': 1080,
                           'fps': 60}
        
        self.frame_number = 0
        #self.spthreshold = spthreshold
        #y = np.linspace(0, self.properties['height'], num=self.properties['height'])
        #x = np.linspace(0, self.properties['width'], self.properties['width'])
        #X, Y = np.meshgrid(x, y)
        #self.noise_angle = 2.0*np.pi*(20*Y + 2*X)
        
    def __iter__(self):
        return self

    def __next__(self):
        """
        Función iteradora, cada vez que es llamada lee y retorna un frame de video
        
        Termina cuando el video ha sido consumido por completo
        """
        frame = self.frames[self.frame_number]
        self.frame_number += 1 
        if self.frame_number == len(self.frames):
            self.frame_number = 0 
        return frame

        #periodic_noise = 0.5 + 0.5*np.cos(self.noise_angle  - self.frame_number*0.1)
        #periodic_noise = periodic_noise.reshape(noisy_frame.shape)
        #noisy_frame += periodic_noise
        #noisy_frame /= np.amax(np.abs(noisy_frame))
        
        #spprob = np.random.rand(self.properties['height'], self.properties['width'])
        #smask = spprob > self.spthreshold
        #pmask = spprob < 1. - self.spthreshold
        #noisy_frame[smask] = 1.
        #noisy_frame[pmask] = 0.
        #self.frame_number += 1
    
    def get_resolution(self):
        """
        Retorna una tupla con el alto (filas) y ancho (columnas) del video
        """
        return (self.properties['height'], self.properties['width'])
    
    def get_fps(self):
        """
        Retorna los cuadros por segundo (fps) del video
        """
        return self.properties['fps']
       
    def __del__(self):
        del self.frames
