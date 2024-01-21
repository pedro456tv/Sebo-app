from flask import Flask, render_template, request
from PIL import Image
import os
import random

app = Flask(__name__,static_folder='static')

all_words = slovak_words = ["Ahoj","Čašník","Kniha","Slnečnica","Voda","Stôl","Okno","Hory","Ryba","Sliepka","Vlk","Krása","Dom",
                            "Počítač","Jablko","Kvet","Mesto","Hudba","Rýchlosť","Trh"]


selected_words = random.sample(all_words, 10)
numbers = list(range(1, 150)) 
random.shuffle(numbers)  
assignments = {word: numbers.pop() for word in selected_words}
IMAGE_FOLDER = 'static/images'
NUM_IMAGES_TO_DISPLAY = 24
NUM_IMAGES_IN_SECOND_SET = 16


def resize_images(input_folder, output_folder, target_size):
    
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Open the image
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize(target_size)

            # Save the resized image
            resized_img.save(output_path)


resize_images(IMAGE_FOLDER, IMAGE_FOLDER, (150, 150))

@app.route('/')
def home():
    return render_template('home.html')

def modify_sentence(sentence):
    # Create a list of words in the sentence
    words = sentence.split()

    # Calculate the number of words to blank out
    words_to_blank = max(1, int(len(words) / 2)-1)

    # Get indices of words to blank out
    word_indices = list(range(len(words)))

    # Ensure no two blank words are next to each other
    blank_indices = []
    while len(blank_indices) < words_to_blank:
        index = random.choice(word_indices)
        if index not in blank_indices:
            if index - 1 not in blank_indices and index + 1 not in blank_indices:
                blank_indices.append(index)

    # Replace selected indices with '_____'
    for index in blank_indices:
        words[index] = '_____'

    # Join the words back into a sentence
    modified_sentence = ' '.join(words)

    return modified_sentence

def generate_array(array_size):
    return [random.randint(0, 9) for _ in range(array_size)]

def generate_rows(num_rows, start_size, end_size):
    rows = []
    for i in range(num_rows):
        row = []
        for size in range(start_size, end_size + 1):
            row.append(generate_array(size))
        rows.append(row)
    return rows

def get_random_images(folder, num_images):
    image_files = sorted(folder)
    selected_images = random.sample(image_files, min(num_images, len(image_files)))
    return selected_images

@app.route('/section1')
def section1():
    
    placements = []
    for i in range(40):
        riadok = random.randrange(3)
        stlpec = random.randrange(3)
        placements.append((riadok,stlpec))
    
    grids = []
    for _ in range(40):
        grid = [['#' for _ in range(3)] for _ in range(3)]
        x,y = placements[_]
        grid[x][y] = 'X'
        result = '\n'.join([''.join(row) for row in grid])
        grids.append(result)
    
    return render_template('section1.html', grids=grids)

@app.route('/section2')
def section2():
    selected_words = random.sample(all_words, 10)
    numbers = list(range(1, 150)) 
    random.shuffle(numbers)  
    assignments = {word: numbers.pop() for word in selected_words}
    display_choices = [random.choice(["word", "number"]) for _ in range(10)]
    return render_template('section2.html',assignments=assignments,display_choices=display_choices)

@app.route('/section3', methods=['GET', 'POST'])
def section3():
    if request.method == 'POST':
        # Get the user input from the form
        original_text = request.form.get('user_input')

        # Split the text into sentences
        sentences = original_text.split('.')

        # Modify each sentence
        modified_sentences = [modify_sentence(sentence) for sentence in sentences if sentence.strip()]

        # Join the modified sentences back into text
        modified_text = '. '.join(modified_sentences)

        return render_template('section3.html', original_text=original_text, modified_text=modified_text)

    # If it's a GET request, just render the form
    return render_template('section3.html')

@app.route('/section4')
def section4():
    num_rows = 10
    start_size = 3
    end_size = 9

    # Generate rows with arrays of consecutive sizes
    rows = generate_rows(num_rows, start_size, end_size)

    return render_template('section4.html', rows=rows)

@app.route('/section5')
def section5():
    # Get the first set of 24 images
    image_files = os.listdir(IMAGE_FOLDER)
    first_set_images = get_random_images(image_files, NUM_IMAGES_TO_DISPLAY)

    # Get the second set of 16 images
    remaining_images = set(os.listdir(IMAGE_FOLDER)) - set(first_set_images)
    second_set_images = get_random_images(remaining_images, NUM_IMAGES_IN_SECOND_SET//2) + get_random_images(first_set_images, NUM_IMAGES_IN_SECOND_SET//2)
    random.shuffle(second_set_images)
    return render_template('section5.html', first_set_images=first_set_images, second_set_images=second_set_images)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
