#this program will create 2 folders in the directory the program is launched from: xkcd_serial and xkcd_async
#In my testing, Async has a 4-5x speed increase over serial. I have only tested with ~100 images though.
#you can edit lowerBound and upperBound to change the range of images downloaded.

#I decided to build the links into a list first, since it seems much faster than having to access the same webpages twice (once for serial, once for async)

from turtle import up
import requests, os, bs4
import time
import asyncio
import aiohttp
import aiofiles

lowerBound = 100
upperBound = 200


links = []

def buildLinks(start, end):
    print("Getting links....")
    url = 'https://xkcd.com' # starting url
    for page in range(start,end): 
        # Download the page.
        if page == 404: #404 is not valid number
            continue
        pageURL= url + "/" + str(page)
        #print('Getting link for page %s...' % pageURL)
        res = requests.get(pageURL)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Find the URL of the comic image.
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            comicUrl = 'https:' + comicElem[0].get('src')
            links.append(comicUrl)
    print("Done.")
    return(links)


def serialDownload(links):
    os.makedirs('xkcd_serial', exist_ok=True) # store comics in ./xkcd
    startTime = time.time()
    for page in links: 


        # Download the image.
        #print('Downloading image %s...' % (page[29:]))
        res = requests.get(page)
        res.raise_for_status()

        # Save the image to ./xkcd.
        #https://imgs.xkcd.com/comics/meerkat.jpg
        imageFile = open(os.path.join('xkcd_serial', page[29:]), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    stopTime = time.time()
    #print('time to complete: %s' % (stopTime - startTime))
    return(stopTime - startTime)
    
async def downloadAsync(url, session):
    async with session.get(url) as response:
        async with aiofiles.open(os.path.join('xkcd_async', url[29:]), 'wb') as file:
                await file.write(await response.read())

async def setupAsync(links):
       async with aiohttp.ClientSession() as session:
           await asyncio.gather(
               *[downloadAsync(file, session) for file in links]
           )

if __name__ =="__main__":
    os.makedirs('xkcd_serial', exist_ok=True)
    os.makedirs('xkcd_async', exist_ok=True) 
    
    buildLinks(lowerBound, upperBound)

    print("Starting serial download of images!")
    serialtime = serialDownload(links)

    print("Starting async download of images!")
    loop = asyncio.get_event_loop()
    start_time = time.time()
    loop.run_until_complete(setupAsync(links))
    async_time = time.time() - start_time

    print(f"Time to complete Serial: {serialtime}")
    print(f"Time to complete Async: {async_time}")
    
    print(f"Async speedup: {serialtime/async_time}")
    syncSize = 0
    asyncSize = 0

    for elements in os.scandir(os.path.join(os.getcwd(), "xkcd_serial")):
        syncSize += os.path.getsize(elements)
    for elements in os.scandir(os.path.join(os.getcwd(), "xkcd_async")):
        asyncSize += os.path.getsize(elements)
    
    if(asyncSize == syncSize):
        print("Downloaded files are the same!")
    else:
        print("Downloaded files are not the same!")