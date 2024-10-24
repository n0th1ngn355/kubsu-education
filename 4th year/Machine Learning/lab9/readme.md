```cmd
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
python train.py --img 640 --epochs 3 --data coco128.yaml --weights yolov5s.pt
```

далее смотрим в runs/train/exp/ и берем например results.png