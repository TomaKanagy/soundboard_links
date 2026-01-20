import argparse
import csv
#for whatever reason, plyance thinks vlc is installed in the wrong location, but everything works so just ignore the error message.
import vlc #type: ignore

def main():
    command_line()
    locations_menu()


#reads program for command-line arguments and adds sound bites
def command_line():
    #Write -help menu and parse command-line for --add argument
    parser = argparse.ArgumentParser(description= "Digital soundboard with sound bites from various songs 🎵")
    parser.add_argument("--add", help= "Add your own sound bite via direct link to an audio file. This can be accomplished by adding the file to your github, then filling the in blanks to this direct link format: https://raw.githubusercontent.com/<your_Github_username>/<your_repository_name>/<branch_name>/<file_name>.<extension_name(like m4a or mp3)>\nMake sure the file is public!")
    args = parser.parse_args()

    #adds sound bite to a csv file with format: location, title, link
    if args.add is not None:
        #asks user for title and locaiton of soundbite
        title = input("What would you like to call this sound bite? ")
        location = input("Which folder would you like to store this sound bite in? ")
        #accesses csv and writes location, title, link.
        with open("soundboard.csv", "a") as soundboard:
            writer = csv.DictWriter(soundboard, fieldnames=["location", "title", "link"])
            writer.writerow({"location": location, "title": title, "link": args.add})




def locations_menu():
    with open("soundboard.csv", "r") as soundboard:
        reader = csv.DictReader(soundboard, fieldnames=["location", "title", "link"])
        locations = []
        n = 0
        for row in reader:
            if row["location"] not in locations:
                n += 1
                print(f"[{n}] {row['location']}")
                locations.append(row["location"])
            else:
                pass
        location_number = int(input("Please enter the number of the folder you would like to open: "))
        user_location = locations[location_number - 1]
    titles_menu(user_location)



def titles_menu(location):
    with open("soundboard.csv", "r") as soundboard:
        reader = csv.DictReader(soundboard, fieldnames=["location", "title", "link"])
        titles = []
        n = 0
        for row in reader:
            if row["location"] == location:
                n += 1
                print(f"[{n}] {row['title']}")
                titles.append(row["link"])
            else:
                pass
        link_number = int(input("Please enter the number of the sound bite you would like to access: "))
        user_link = titles[link_number - 1]
    play_file(user_link)



#plays the specified link
def play_file(link):
        #vlc prints some fake error message depending on where the direct link comes from, the next three lines instantiates a vlc object such that vlc prints no error messages, creates a new media player from that instantiation, creates a media object from a link, and loads that media object into the media player
        instance = vlc.Instance("--quiet", "--logfile=NUL")
        player = instance.media_player_new()
        player.set_media(instance.media_new(link))

        player.play()
        input("press enter to stop ")

        
if __name__ == "__main__":
    main()
