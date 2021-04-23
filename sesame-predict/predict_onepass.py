import sys, os, subprocess, csv

#while True:
#    joke = input("Enter a joke: ")
#    if len(joke.split(" ")) > 4 and len(joke.split("\n")) == 1:
#        break
#    print("invalid input")

targetid_model = "fn1.7-targetid"
frameid_model = "fn1.7-frameid"
frameid_adam_model = "fn1.7-frameid-adam"
argid_model = "fn1.7-argid"
filename = os.path.abspath(os.path.dirname(__file__)) + "/sentences.txt"
resultfilename = os.path.abspath(os.path.dirname(__file__)) + "/frames.txt"

os.chdir("../open-sesame")

#with open(filename, "w") as fout:
#    fout.write(joke)

targetid_model_filename = f"logs/{targetid_model}/predicted-targets.conll"
frameid_model_filename = f"logs/{frameid_model}/predicted-frames.conll"
argid_model_filename = f"logs/{argid_model}/predicted-args.conll"
frameid_adam_model_filename = f"logs/{frameid_adam_model}/predicted-frames.conll"

def write_results(input_file, outputfile):
    with open(outputfile, 'w+') as writer:
        joke_frames = []
        frames = []
        with open(targetid_model_filename, newline='') as targetfile, open(input_file, newline='') as jokefile, open(argid_model_filename, newline='') as csvfile:
            targetlines = [line.strip() for line in targetfile]
            jokes = [line.strip() for line in jokefile]
            csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            index_target = 0
            joke_index = 0
            taged_text = {}
            for i, row in enumerate(csvreader):
                index_target += 1
                try:
                    if targetlines[index_target].strip() == "%":
                        frames.append(taged_text)
                        taged_text = {}
                        joke_frames.append(frames)
                        frames = []
                        index_target += 1
                        joke_index += 1
                        continue
                except IndexError:
                    pass

                if len(row) == 0:
                    frames.append(taged_text)
                    taged_text = {}
                    continue
                
                tag = (row[-2] if row[-3] != "_" else (row[-1].split("-")[1] if "-" in row[-1] else row[-1])).lower().replace("_", " ")
                text = (row[3] if row[3].lower() != "unk" else row[1]).lower()

                if tag in taged_text:
                    taged_text[tag] = f"{taged_text[tag]} {text}"
                else:
                    taged_text[tag] = f"{text}"


        for index, frames_temp in enumerate(joke_frames):
            writer.writelines([f"\nJoke: {jokes[index]}\n--------------------------------------------------------------------------------------\n"])
            for i, frame in enumerate(frames_temp):
                writer.writelines([f"\nFRAME {i + 1} ------------------------------\n"])
                writer.writelines([f"{value} - {key}\n" for key, value in frame.items() if key != "o"])
            writer.writelines([f"\n--------------------------------------------------------------------------------------\n"])


def call_sesame(command, model, file):
    args = [
        "python",
        "-m",
        f"sesame.{command}",
        "--mode",
        "predict",
        "--model_name",
        model,
        "--raw_input",
        file
    ]
    
    print(str.join(" ", args))

    process = subprocess.Popen(args=args, 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        return_code = process.poll()
        if return_code is not None:
            for output in process.stdout.readlines():
                print(output.strip())
            break

def parse_file(input_file, output_file):
    call_sesame("targetid", targetid_model, input_file)
    call_sesame("frameid", frameid_model, targetid_model_filename)
    call_sesame("argid", argid_model, frameid_model_filename)

    write_results(input_file, output_file)


if __name__ == "__main__":
    parse_file(filename, resultfilename)
