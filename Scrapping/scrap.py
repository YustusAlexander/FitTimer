import json
import os.path
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.2.834 Yowser/2.5 Safari/537.36"
}


def save_pages():
    global headers
    url = "https://www.jefit.com/exercises/bodypart.php?id=11&exercises=All&All=0&Bands=0&Bench=0&Dumbbell=0&EZBar=0&Kettlebell=0&MachineStrength=0&MachineCardio=0&Barbell=0&BodyOnly=0&ExerciseBall=0&FoamRoll=0&PullBar=0&WeightPlate=0&Other=0&Strength=0&Stretching=0&Powerlifting=0&OlympicWeightLifting=0&Beginner=0&Intermediate=0&Expert=0&page="
    for page in tqdm(range(1, 131)):
        if os.path.exists(f"pages/{page}.html") == False:
            req = requests.get(url + str(page), headers=headers)
            src = req.text
            with open(f"pages/{page}.html", "w", encoding="UTF-8") as file:
                 file.write(src)
        else:
            print(f"файл {page}.html уже существует!")


def scrap_exercises():
    global headers
    exercises_dict = {}
    exercise_id = 100

    # search info
    for page in tqdm(range(1, 131)):
        with open(f"pages/{page}.html", encoding="UTF-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        all_row = soup.find_all("tr")
        # print(all_row)
        for item in all_row[2:]:
            teg_img = item.find("img")
            img_src1 = "https://www.jefit.com" + teg_img.get("src")[2:]
            num2_img = str(int(teg_img.get("src")[2:-4].split("/")[-1]) + 1)
            img_src2 = "https://www.jefit.com" + teg_img.get("src")[2:-(len(num2_img)+4)] + num2_img + teg_img.get("src")[-4:]
            Name_Exercise = item.find("a").get("title")
            Main_Muscle_Group = item.find_all("p")[0].text.split(':')[-1].strip()
            Type_Exercise  = item.find_all("p")[1].text.split(':')[-1].strip()
            Equipment = item.find_all("p")[2].text.split(':')[-1].strip()
            # print(Name_Exercise, img_src1, img_src2, Main_Muscle_Group, Type_Exercise, Equipment)

            # save img
            try:
                if os.path.exists(f"json/media/{exercise_id}_1.jpg") == False:
                    req = requests.get(url=img_src1, headers=headers)
                    response = req.content
                    with open(f"json/media/{exercise_id}_1.jpg", "wb") as file:
                        file.write(response)
                if os.path.exists(f"json/media/{exercise_id}_2.jpg") == False:
                    req = requests.get(url=img_src2, headers=headers)
                    response = req.content
                    with open(f"json/media/{exercise_id}_2.jpg", "wb") as file:
                        file.write(response)
            except:
                print(f"ошибка {exercise_id}")

            # create dictionary
            exercises_dict[exercise_id] = [
                    Name_Exercise,
                    {"Img": (f"/media/{exercise_id}_1.jpg", f"/media/{exercise_id}_2.jpg")},
                    {"Main_Muscle_Group": Main_Muscle_Group},
                    {"Type_Exercise": Type_Exercise},
                    {"Equipment": Equipment}
            ]

            exercise_id += 1
    # print(exercises_dict)
    with open("json/exercises_dict.json", "w", encoding="UTF-8") as file:
        json.dump(exercises_dict, file, indent=4, ensure_ascii=False)



def main():
    #save_pages()
    scrap_exercises()


if __name__ == '__main__':
    main()