import requests

class Post:
    def __init__(self, target_url):
        '''
        初期化
        '''
        print("[Post]<__init__>: fire")
        self.target_url = target_url

    def post(self, file_path):
        print("[Post]<post>: fire")
        files = {'upload_file': open(file_path, "rb")}
        res = requests.post(self.target_url, files=files)
        print("送信done")
        return res

if __name__ == "__main__":
    poster = Post("http://localhost:3000")
    poster.post("test.jpg")