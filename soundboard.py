import argparse
import csv
import sys
import os
#for whatever reason, plyance thinks vlc is installed in the wrong location, but everything works so I just ignore the error message.
import vlc #type: ignore


def main():
    command_line()
    play_file(titles_menu(locations_menu()))


#reads program for command-line arguments and adds sound bites
def command_line():
    #Write -help menu and parse command-line for --add argument
    parser = argparse.ArgumentParser(description= "Digital soundboard with sound bites from various songs 🎵. Requires download of VLC (64 bit version). If the link is not playing, it is likely not a valid direct link, not public if linked to github, or the 64 bit version of VLC player is not installed.")
    parser.add_argument("--add", help= 'Add your own sound bite via direct link to an audio file. This can be accomplished by adding the file to your github, then filling the in blanks to this direct link format (include double quotes): \"https://raw.githubusercontent.com/<your_Github_username>/<your_repository_name>/<branch_name>/<folder_name(if no folder skip)><file_name>.<extension_name(like m4a or mp3)>\" Make sure the file is public!')
    parser.add_argument("--delete", help= "Delete unwanted soundbites.", nargs= "?", const=True)
    args = parser.parse_args()

    #adds sound bite to a csv file with format: location, title, link
    if args.add:
        #asks user for title and locaiton of soundbite
        title = input("What would you like to call this sound bite? ")
        try:
            location = locations_menu("Where would you like to store this sound bite? ")                
        except FileNotFoundError:
            print("It looks like you have'nt saved any sound bites yet")
            location = input("What would you like to call your first folder? ")
        #accesses csv and writes location, title, link.
        with open("soundboard.csv", "a") as soundboard:
            writer = csv.DictWriter(soundboard, fieldnames=["location", "title", "link"])
            writer.writerow({"location": location, "title": title, "link": args.add})
        sys.exit("Sucessfully Added")

    if args.delete:
        #asks user for file they wish to delete
        unwanted_file = titles_menu(locations_menu("Please enter the number of the folder in which your unwanted file is stored: "), message= "Please enter the number of the sound bite you would like to delete: ")
        #deleted unwanted file
        with open("soundboard.csv", "r") as input_soundboard, open("blankspace_soundboard.csv", "w") as deleted_soundboard:
            input_reader = csv.DictReader(input_soundboard, fieldnames=["location", "title", "link"])
            blankspace_writer = csv.DictWriter(deleted_soundboard, fieldnames=["location", "title", "link"])
            for row in input_reader:
                if row["link"] != unwanted_file:
                    blankspace_writer.writerow({"location": row["location"], "title": row["title"], "link": row["link"]})  
        #rename deleted_soundboard.csv to soundboard.csv and delete the duplicate with the empty lines
        os.remove("soundboard.csv")
        os.rename("blankspace_soundboard.csv", "soundboard.csv")
        sys.exit("Sucessfully Deleted")





def locations_menu(message="Please enter the number of the folder you would like to open: "):
    with open("soundboard.csv", "r") as soundboard:
        reader = csv.DictReader(soundboard, fieldnames=["location", "title", "link"])
        locations = []
        n = 0
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for row in reader:
            if row["location"] not in locations:
                n += 1
                print(f"[{n}] {row['location']}")
                locations.append(row["location"])
            else:
                pass
        while True:
            try:
                location_number = int(input(message))
                if 0 < location_number <= n:
                    break
                else:
                    message = "Please try again with a valid folder number: "
            except ValueError:
                message = "Please try again with a valid folder number: "
        return locations[location_number - 1]




def titles_menu(location, message= "Please enter the number of the sound bite you would like to access: "):
    with open("soundboard.csv", "r") as soundboard:
        reader = csv.DictReader(soundboard, fieldnames=["location", "title", "link"])
        titles = []
        n = 0
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for row in reader:
            if row["location"] == location:
                n += 1
                print(f"[{n}] {row['title']}")
                titles.append(row["link"])
        while True:
            try:
                link_number = int(input(message))
                if 0 < link_number <= n:
                    break
                else:
                    message = "Please try again with a valid sound bite number: "
            except ValueError:
                message = "Please try again with a valid sound bite number: "
        return titles[link_number - 1]



#plays the specified link
def play_file(link):
        #vlc sometimes prints unnecessary error messages depending on where the direct link comes from, the next three lines instantiates a vlc object such that vlc prints no error messages, creates a new media player from that instantiation, creates a media object from a link, and loads that media object into the media player
        instance = vlc.Instance("--quiet", "--logfile=NUL")
        player = instance.media_player_new()
        player.set_media(instance.media_new(link))
        player.play()
        input("press enter to stop ")

        
if __name__ == "__main__":
    main()
