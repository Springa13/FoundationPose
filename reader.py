from Utils import *

class DTwinReader:
    def __init__(self, video_dir, downscale=1, shorter_side=None, zfar=np.inf):
        self.video_dir = video_dir
        self.downscale = downscale
        self.zfar = zfar
        self.color_files = sorted(glob.glob(f'{self.video_dir}/rgb/*.png'))
        self.K = np.loadtxt(f'{video_dir}/cam_K.txt').reshape(3,3)
        self.count = 0
        self.video_detected = False
        self.shorter_side = shorter_side
    
    def get_first_frame(self):
        
        if os.path.isfile(self.color_files[self.count]):
           
            self.H,self.W = cv2.imread(self.color_files[self.count]).shape[:2]
            
            if self.shorter_side is not None:
                self.downscale = self.shorter_side/min(self.H, self.W)

            self.H = int(self.H*self.downscale)
            self.W = int(self.W*self.downscale)
            self.K[:2] *= self.downscale
            self.video_detected = True
    
    def get_color(self):
        color = imageio.imread(self.color_files[self.count])[...,:3]
        color = cv2.resize(color, (self.W, self.H), interpolation=cv2.INTER_NEAREST)
        return color

    def get_depth(self):
        depth = cv2.imread(self.color_files[self.count].replace('rgb','depth'),-1)/1e3
        depth = cv2.resize(depth, (self.W, self.H), interpolation=cv2.INTER_NEAREST)
        depth[(depth<0.001) | (depth>=self.zfar)] = 0
        return depth

    def get_mask(self):
        mask = cv2.imread(self.color_files[i].replace('rgb','masks'),-1)
        if len(mask.shape)==3:
            for c in range(3):
                if mask[...,c].sum()>0:
                    mask = mask[...,c]
                    break
        mask = cv2.resize(mask, (self.W,self.H), interpolation=cv2.INTER_NEAREST).astype(bool).astype(np.uint8)
        return mask

    def increment_count(self):
        self.count += 1

    def get_video_detected(self):
        return self.video_detected

    def get_next_frame_exists(self):
        rgbExists = os.path.isfile(self.color_files[self.count])
        depthExists = os.path.isfile(self.color_files[self.count].replace('rgb','depth'))
        return rgbExists
    
    def get_count(self):
        return self.count

    def get_current_file(self):
        return self.color_files[self.count]
        
       