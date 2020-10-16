## Get Article Title from URL Link

Original Author: James Sullivan

This script is used to extract a news article title from a URL (contained in an attribute field, “url”), and was developed specifically for articles cataloged in the [GDELT project](https://www.gdeltproject.org/) and accessed through their API. In order for it to work, the article name must be included in the URL. In general, the script works backwards from the end of the URL, splits on the “/,” identifies the title based on the “-“ character separating the words, does some formatting, then reassembles the title back together. The script will handle a few different formats and unique cases.

For example:

https://www.forbesindia.com/article/take-one-big-story-of-the-day/drones-waft-in-a-world-of-virtual-dealmaking/63285/1

This case is fairly straight forward, and the script will split on the “/” then find the first “-“ and pull the title from that. There isn’t much clean up required.

https://www.thehour.com/news/article/State-police-ID-couple-in-murder-suicide-15628872.php

In this case, there’s some additional error checking for the number at the end of the title, “15628872,” that will be identified based on the “.” as not being part of the title and discarded.

https://www.syracuse.com/business/2020/10/israeli-drone-company-to-open-control-center-in-syracuse.html

In this example, when the “.” is identified the script will determine that the text connected to it, “syracuse” is actually part of the title and will be held on to.

https://www.theepochtimes.com/boy-5-sends-baby-yoda-doll-to-front-line-oregon-firefighters-in-case-you-get-lonely_3519946.html

In this example, the number at the end, “3519946,” is not meant to be part of the title, but is connected by a “_” and not a “-“ like the previous example. The script can handle this as well by replacing all “_” with a “-“ because splitting the title out.
