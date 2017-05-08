#include "ros/ros.h"
#include "opencv2/opencv.hpp"
#include "std_msgs/String.h"
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include "HsvAdjust.hpp"

using namespace std;
using namespace cv;

void trackBall()
{
    //HsvAdjust adjust;
    //adjust.grabWebcamImage("src/uas_project/src/hej.jpg");
}

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
  try
  {
  	Mat img = cv_bridge::toCvShare(msg, "bgr8")->image;  // Convert from ROS message to openCV image
    HsvAdjust adjust;
    adjust.hsvSegmentation(img);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
  }
}


int main(int argc, char **argv)
{
    ros::init(argc, argv, "image_listener"); // Init ROS
    ros::NodeHandle nh; // Node handler
    image_transport::ImageTransport it(nh);
    image_transport::Subscriber sub = it.subscribe("camera_image", 5, imageCallback);   // Image receiver

    ros::spin();
}
