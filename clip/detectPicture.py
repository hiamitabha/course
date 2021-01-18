"""./detectPicture.py can be used to take pictures from the Anki robot's camera and detect the main object in the picture with the help of OpenAI's clip library
"""
# Copyright (c) 2020 Amitabha Banerjee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import anki_vector
import argparse
import time
import torch
import clip
from PIL import Image
from anki_vector.util import degrees

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def detectPicture(robot, choiceStr):
   vectorImage = robot.camera.capture_single_image()
   image = preprocess(vectorImage.raw_image).unsqueeze(0).to(device)
   with torch.no_grad():
      image_features = model.encode_image(image)
      text = clip.tokenize(choiceStr).to(device)
      text_features = model.encode_text(text)
    
      logits_per_image, logits_per_text = model(image, text)
      probs = logits_per_image.softmax(dim=-1).cpu().numpy()

   for text, prob in zip(choiceStr, probs[0]):
      print(text + ":" + "{:.2f}".format(prob))    

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("-c", "--choiceString",
                       help="A common separate representation of the strings that we need the image classified for",
                       default="my favorite vector,my vector")
   args = anki_vector.util.parse_command_args(parser)
   choiceStr = args.choiceString.split(",")
   with anki_vector.Robot(serial=args.serial) as robot:
      robot.behavior.set_head_angle(degrees(13.0))
      detectPicture(robot, choiceStr)

   
