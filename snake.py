# Made by : Muhammad Fazeel
# Reg No  : 453385
# Course  : Artificial Intelligence

import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("512x542")  
        self.master.resizable(False, False)

        self.score = 0
        self.adv_score = 0
        self.game_duration = 180  

        self.create_widgets()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.obstacle_L_shape = [(200, 200), (200, 220), (200, 240), (220, 240), (240, 240)]
        self.obstacle_I_shape = [(100, 200), (100, 220), (100, 240), (100, 260), (100, 280), (100, 300)]

        self.direction = "Right"

        self.adversarial_snake = [(400, 400), (410, 400), (420, 400)]
        self.adversarial_direction = "Left"

        self.food = self.create_food()
        self.food_coord = self.canvas.coords(self.food)

        self.master.bind("<KeyPress>", self.change_direction)

        self.center_window()

        self.adversarial_speed = 200
        self.start_time = time.time() 
        self.update()

    def create_widgets(self):
        self.score_frame = tk.Frame(self.master, bg="black")
        self.score_frame.pack(fill=tk.X)

        self.score_label = tk.Label(self.score_frame, text="Score: 0", bg="black", fg="white")
        self.score_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.adv_score_label = tk.Label(self.score_frame, text="Adversarial Score: 0", bg="black", fg="white")
        self.adv_score_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.timer_label = tk.Label(self.master, text="Time: 3:00", font=("Helvetica", 12), bg="black", fg="white")
        self.timer_label.pack(pady=10)

        self.canvas = tk.Canvas(self.master, bg="black", width=500, height=500)
        self.canvas.pack(pady=6)

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart)
        self.restart_button.pack(side=tk.TOP, pady=10)

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width - 512) // 2
        y = (screen_height - 542) // 2  
        self.master.geometry("512x542+{}+{}".format(x, y))

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tags="food")
        if (x, y) in self.obstacle_L_shape or (x, y) in self.obstacle_I_shape or (x, y) in self.snake or (
                x, y) in self.adversarial_snake:
            self.canvas.delete(food)
            food = self.create_food()
        return food

    def update_score(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def update_adversarial_score(self):
        self.adv_score += 1
        self.adv_score_label.config(text=f"Adversarial Score: {self.adv_score}")

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)
        self.snake.pop()

    def move_adversarial_snake(self):
        head = self.adversarial_snake[0]

        path = self.find_path(head, (self.food_coord[0], self.food_coord[1]),
                               self.obstacle_L_shape + self.obstacle_I_shape + self.adversarial_snake[1:])
        if path:
            new_head = path[1] if len(path) > 1 else head
        else:
            new_head = self.random_move(head)

        self.adversarial_snake.insert(0, new_head)

        if len(self.adversarial_snake) > 10:
            self.adversarial_snake.pop()

    def random_move(self, head):
        possible_moves = [
            (head[0] + 20, head[1]),
            (head[0] - 20, head[1]),
            (head[0], head[1] + 20),
            (head[0], head[1] - 20),
        ]
        return random.choice(possible_moves)

    def find_path(self, start, target, obstacles):
        open_set = [start]
        came_from = {}

        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}

        while open_set:
            current = min(open_set, key=lambda x: f_score[x])

            if current == target:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            open_set.remove(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in obstacles:
                    continue 

                tentative_g_score = g_score[current] + self.distance(current, neighbor)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, target)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

        return None

    def get_neighbors(self, position):
        x, y = position
        return [
            (x + 20, y),
            (x - 20, y),
            (x, y + 20),
            (x, y - 20),
        ]

    def distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def heuristic(self, pos1, pos2):
        return self.distance(pos1, pos2)

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, self.game_duration - elapsed_time)
        minutes, seconds = divmod(remaining_time, 60)
        timer_str = f"Time: {minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=timer_str)
        self.elapsed_time = elapsed_time

    def update(self):
        self.move_snake()

        head = self.snake[0]

        if (
                len(head) < 2 or
                head in self.snake[1:]
                or head[0] < 0
                or head[0] > 480
                or head[1] < 0
                or head[1] > 480
                or head in self.obstacle_L_shape
                or head in self.obstacle_I_shape
        ):
            self.end_game("Player crashed the snake! AI wins!")
            return

        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake"
            )

        self.canvas.delete("obstacle")
        for segment in self.obstacle_L_shape:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tags="obstacle"
            )
        for segment in self.obstacle_I_shape:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tags="obstacle"
            )

        food_coords = self.canvas.coords(self.food)
        if len(head) >= 2 and head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))
            self.canvas.delete("food")
            self.food = self.create_food()
            self.food_coord = self.canvas.coords(self.food)
            self.update_score()

        self.move_adversarial_snake()
        adversarial_head = self.adversarial_snake[0]

        if (
                adversarial_head in self.adversarial_snake[1:]
                or adversarial_head[0] < 0
                or adversarial_head[0] > 480
                or adversarial_head[1] < 0
                or adversarial_head[1] > 480
                or adversarial_head in self.obstacle_L_shape
                or adversarial_head in self.obstacle_I_shape
        ):
            self.end_game("AI crashed the snake! Player wins!")
            return

        if len(adversarial_head) >= 2 and adversarial_head[0] == food_coords[0] and adversarial_head[1] == food_coords[
            1]:
            self.adversarial_snake.append((0, 0))
            self.canvas.delete("food")
            self.food = self.create_food()
            self.food_coord = self.canvas.coords(self.food)
            self.update_adversarial_score()

        self.canvas.delete("adversarial_snake")
        for segment in self.adversarial_snake:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="purple", tags="adversarial_snake"
            )

        self.update_timer()

        if self.elapsed_time >= self.game_duration:
            player_score = self.score
            ai_score = self.adv_score
            if player_score > ai_score:
                self.end_game("Time's up! Player wins!")
            elif ai_score > player_score:
                self.end_game("Time's up! AI wins!")
            else:
                self.end_game("Time's up! It's a tie!")

        else:
            self.master.after(200, self.update)

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def end_game(self, message):
        self.canvas.grid_remove()
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height()/4,
            text=f"{message}\nYour Score is: {self.score}\nAdversarial Score is: {self.adv_score}",
            fill="white"
        )
        self.restart_button.place(relx=0.5, rely=0.5, anchor='center')

    def restart(self):
        self.restart_button.place_forget()
        self.canvas.delete("all")
        self.start_time = time.time()
        self.score = 0
        self.adv_score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.adv_score_label.config(text=f"Adversarial Score: {self.adv_score}")
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.adversarial_snake = [(400, 400), (410, 400), (420, 400)]
        self.obstacle_L_shape = [(200, 200), (200, 220), (200, 240), (220, 240), (240, 240)]
        self.obstacle_I_shape = [(100, 200), (100, 220), (100, 240), (100, 260), (100, 280), (100, 300)]
        self.direction = "Right"
        self.adversarial_direction = "Left"
        self.food = self.create_food()
        self.food_coord = self.canvas.coords(self.food)
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
        
