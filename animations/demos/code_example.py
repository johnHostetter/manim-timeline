from manim import *


# https://stackoverflow.com/questions/75363537/fix-long-text-and-distorted-text-in-manim
class MyCode(Scene):
    def construct(self):
        NN_text = """
        import torch
        hidden_size: int = 16
        model = torch.nn.Sequential(
            torch.nn.Linear(4, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, 1)
        )
        """
        # NN_text = """
        # import keras
        # from keras.models import Sequential
        # from keras. layers import Dense
        # model = Sequential ()
        # n_cols = concrete_data. shape [1]
        # model. add (Dense (5, activation='relu',
        # model. add (Dense(5, activations' reluj, input_shape=(n_ (cols, )))
        # model.add(Dense (1))
        # model. compile (optimizer='adam', loss='mean_squared_error')
        # model.fit (predictors, target)
        # predictions = model.predict(test_data)
        # """
        code_text = Code(
            code=NN_text,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=False,
            style=Code.styles_list[15],
            background="window",
            language="python",
            font="consolas",
            font_size=18,
        )
        self.play(Write(code_text), run_time=5)
        self.wait()
        for obj in code_text[2]:
            self.play(Wiggle(obj))
        self.wait()


if __name__ == "__main__":
    my_code = MyCode()
    my_code.render()
