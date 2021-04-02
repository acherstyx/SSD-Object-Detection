import unittest

from data_loaders.ssd import SSDDataset
from models.ssd_model import *


class TestSSDObjectDetectionModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.model = SSDObjectDetectionModel(classes=80, learning_rate=0.0001)
        self.model.show_summary()

        self.dummy_input = tf.random.normal([5, 300, 300, 3])
        self.dummy_output = self.model.get_tf_model()(self.dummy_input)

        try:
            self.coco_dataset_train, self.coco_dataset_val = SSDDataset("./datasets/coco").get_dataset()
        except ValueError:
            self.coco_dataset_train, self.coco_dataset_val = SSDDataset("../../datasets/coco").get_dataset()

        super().__init__(*args, **kwargs)

    def test_train_set_visualize(self):
        dataset_for_train = self.model.get_train_set(self.coco_dataset_train)
        for image, (cls, bbox, mask) in dataset_for_train:
            result_image = self.model.visualize_dataset(image, cls, bbox, mask)
            cv2.imshow("view", result_image)
            ch = cv2.waitKey(0)
            if ch == "q":
                break

    def test_prior_box(self):
        prior_box = self.model.get_prior_box()

        print("==========prior box==========")
        for i, box in enumerate(prior_box):
            print(i, box)
            # if i > 1000:
            #     break
        print("==========prior box==========")

    def test_prior_box_visualize(self):
        self.model.visualize_prior_box()

    def test_train(self):
        logging.basicConfig(level=logging.DEBUG)
        self.model.train(self.coco_dataset_train, epoch=200, batch_size=8)


if __name__ == '__main__':
    unittest.main()