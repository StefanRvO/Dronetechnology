/*
*   Class for visually adjusting and finding the appropiate HSV segmentation values
*/

#include "HsvAdjust.hpp"

HsvAdjust::HsvAdjust()
{
    hSliderMin = 0;
    hSliderMax = 180;
    sSliderMin = 0;
    sSliderMax = 255;
    vSliderMin = 0;
    vSliderMax = 255;

    areaThresh = 0;
    compactThresh = 0;
}

void HsvAdjust::on_trackbar( int something, void *userdata)
{
    ((HsvAdjust *)(userdata))->on_trackbar(something);
}

void HsvAdjust::on_trackbar( int)
{
    // HSV color segmentation
    cv::inRange(imghsv, cv::Scalar(hSliderMin, sSliderMin, vSliderMin), cv::Scalar(hSliderMax, sSliderMax, vSliderMax), dst);


    Mat im2 = dst;
    im2 = findContours(im2);

    // Print found values
    printValues();

    // Display images
    Mat newImage;
    hconcat(dst, im2, newImage);    // Create a new image containing both images
    imshow("Colour Segmentation", newImage);
}

void HsvAdjust::guiSegmentation(Mat img)
{
    namedWindow("Original", cv::WINDOW_NORMAL);
    imshow("Original", img);
    cv::resizeWindow("Original", 500,500);

    cv::cvtColor(img, imghsv, CV_BGR2HSV);

    namedWindow("Colour Segmentation", cv::WINDOW_NORMAL);
    cv::resizeWindow("Colour Segmentation", 500,500);

    cv::createTrackbar( "Hue min", "Colour Segmentation", &hSliderMin, hSlider, &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "Hue max", "Colour Segmentation", &hSliderMax, hSlider,  &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "S min", "Colour Segmentation", &sSliderMin, sSlider,  &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "S max", "Colour Segmentation", &sSliderMax, sSlider,  &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "V min", "Colour Segmentation", &vSliderMin, vSlider,  &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "V max", "Colour Segmentation", &vSliderMax, vSlider,  &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "Area thresh", "Colour Segmentation", &areaThresh, threshSlider,  &HsvAdjust::on_trackbar, (void *)this);
    cv::createTrackbar( "Compact thresh", "Colour Segmentation", &compactThresh, threshSlider,  &HsvAdjust::on_trackbar, (void *)this);

    cv::waitKey(0);
}

Mat HsvAdjust::findContours(Mat img)
{
    // Find contours
    std::vector<std::vector<cv::Point> > contours;
    std::vector<std::vector<cv::Point> > acceptedContours;
    std::vector<cv::Vec4i> hierarchy;
    cv::findContours( img, contours, hierarchy, CV_RETR_LIST, cv::CHAIN_APPROX_NONE);

    // Draw the contours which have an area within certain limits
    for(unsigned int i = 0; i< contours.size(); i++)
    {
        // Calculate compactness
        float compactness = (4*M_PI * cv::contourArea(contours[i])) / (cv::arcLength(contours[i], true) * cv::arcLength(contours[i], true));

        // Check for how much circle it is and the area size
        if(compactness > (float)(compactThresh/1000) && cv::contourArea(contours[i]) > (float)(areaThresh/1000))
        {
            acceptedContours.push_back(contours[i]);
        }
    }

    // Choose the biggest circle contour
    int largest_area=0;
    vector<Point> largest_contour;

    for(uint i = 0; i< acceptedContours.size(); i++ ) {
        double a=contourArea( acceptedContours[i],false);  //  Find the area of contour
        if(a>largest_area){
            largest_area=a;
            largest_contour = acceptedContours[i];
        }
    }

    // Fra Allan
    vector<Point> contour_poly(contours.size());

    approxPolyDP( Mat(largest_contour), contour_poly, 3, true );

    minEnclosingCircle( (Mat)contour_poly, Center, Radius );

    //c=Center;
    //r=Radius;

    circle( img, Center, (int)Radius, Scalar(255,255,255), 1, 8, 0 );
    return img;
}

Point2f HsvAdjust::getBallPosition(Mat img)
{
    // HSV color segmentation
    cv::cvtColor(img, imghsv, CV_BGR2HSV);
    cv::inRange(imghsv, cv::Scalar(90, 92, 86), cv::Scalar(180, 255, 225), dst);

    // Find contours
    areaThresh = 382;
    compactThresh = 565;
    dst = findContours(dst);

    return Center;
}

void HsvAdjust::printValues()
{
    // Print the found HSV values
    cout << "Hue min: " << hSliderMin << endl;
    cout << "Hue max: " << hSliderMax << endl;
    cout << "Sat min: " << sSliderMin << endl;
    cout << "Sat max: " << sSliderMax << endl;
    cout << "Val min: " << vSliderMin << endl;
    cout << "Val max: " << vSliderMax << endl;
    cout << "Compact Threshold: " << compactThresh << endl;
    cout << "Area Threshold: " << areaThresh << endl;
    cout << "Center: " << Center << endl;
    cout << "Radius: " << Radius << endl;
}
