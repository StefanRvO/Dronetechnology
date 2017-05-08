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

static HsvAdjust adjust;

void trackBall(Mat img)
{
    Mat hsv_img, seg_img;

    /*
    // Find segmentation values
    HsvAdjust adjust;
    adjust.hsvSegmentation(img);*/

    // HSV color segmentation
    cvtColor(img, hsv_img, cv::COLOR_BGR2HSV_FULL); // Convert to HSV image
    inRange(hsv_img, Scalar(119, 22, 121), Scalar(180,255,252), seg_img);

    /*
    // Dilate and erode
    cv::Mat kernel = cv::Mat::ones(3,3,CV_8UC1);
    cv::dilate(inImg,inImg,kernel);
    cv::erode(inImg,inImg,kernel);
    kernel = cv::Mat::ones(13,13,CV_8UC1);
    cv::erode(inImg,inImg,kernel);
    cv::dilate(inImg,inImg,kernel);

    // Find contours
    std::vector<std::vector<cv::Point> > contours;
    std::vector<std::vector<cv::Point> > acceptedContours;
    std::vector<cv::Vec4i> hierarchy;
    cv::findContours( inImg, contours, hierarchy, CV_RETR_LIST, cv::CHAIN_APPROX_NONE);

    // Draw the contours which have an area within certain limits
    for(unsigned int i = 0; i< contours.size(); i++)
    {
        // Calculate compactness
        float compactness = (4*M_PI * cv::contourArea(contours[i])) / (cv::arcLength(contours[i], true) * cv::arcLength(contours[i], true));

        // Check for how much circle it is and the area size
        if(compactness > compactThresh && cv::contourArea(contours[i]) > areaTresh)
        {
            acceptedContours.push_back(contours[i]);
        }
    }*/
}

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
  try
  {
  	Mat img = cv_bridge::toCvShare(msg, "bgr8")->image;  // Convert from ROS message to openCV image
    //imwrite("test.jpg", img); // Save image to disk
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
