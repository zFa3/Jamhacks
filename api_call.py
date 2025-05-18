# https://cloud.google.com/vision?hl=en
import requests
import os
import base64

env = os.environ

API_KEY = env.get("API_KEY")
# image_filename = "driving_image.png"
# Create the request payload
url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

class APICall:
    
    def __init__(self) -> None:
        self.phone_detected = 0

    def make_call(self, image_filename) -> None:
        # Load and encode the image
        with open(f"./test_images/{image_filename}", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        payload = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {"type": "LABEL_DETECTION","maxResults": 10},
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 5}
                    ]
                }
            ]
        }

        # Send the POST request
        response = requests.post(url, json=payload)

        # Parse and print the results
        if response.status_code == 200:
            # print(response.json())
            # print("\n\n\n")
            deteched = False
            jsonified = response.json()

            for label in jsonified['responses'][0].get('labelAnnotations', []):
                if "phone" in label['description'] or "device" in label['description']:
                    deteched = True
                    self.phone_detected += 1
                    break
                # print(f"- {label['description']} ({label['score']:.2f})")

            if not deteched:
                for obj in jsonified['responses'][0].get('localizedObjectAnnotations', []):
                    if "phone" in obj['name'] or "device" in obj['name']:
                        deteched = True
                        self.phone_detected += 1
                        break
                    # print(f"- {obj['name']} ({obj['score']:.2f})")
        else:
            print("Error:", response.status_code, response.text)
    
    def return_call(self, image_filename) -> None:
        # Load and encode the image
        with open(f"./test_images/{image_filename}", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        payload = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {"type": "LABEL_DETECTION","maxResults": 10},
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 5}
                    ]
                }
            ]
        }

        # Send the POST request
        response = requests.post(url, json=payload)

        # Parse and print the results
        if response.status_code == 200:
            # print(response.json())
            # print("\n\n\n")
            deteched = False
            jsonified = response.json()

            for label in jsonified['responses'][0].get('labelAnnotations', []):
                print(f"- {label['description']} ({label['score']:.2f})")

            for obj in jsonified['responses'][0].get('localizedObjectAnnotations', []):
                print(f"- {obj['name']} ({obj['score']:.2f})")
        else:
            print("Error:", response.status_code, response.text)
