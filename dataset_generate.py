import cv2
import pafy

if __name__ == '__main__':

    list_video_url=[]
    list_video_url.append('https://www.youtube.com/watch?v=S-vDsDdCj_0')

    count = 0
    i=0
    for url in list_video_url:
        videoPafy = pafy.new(url)
        best = videoPafy.getbest(preftype="webm")
        video = cv2.VideoCapture(best.url)
        while (True):
            ret, frame = video.read()
            if ret:
                cv2.imwrite('dataset_for_tests/face{:d}.jpg'.format(i), frame)
                count += 60
                video.set(1, count)
                i += 1
            else:
                break
