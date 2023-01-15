import tkinter
import customtkinter
import time

import messages as msg
import lz77
import lz78
import lzw

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # устанавливаем тему приложения
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        # формируем окно
        self.title(msg.APP_TITLE)
        self.geometry(f"{1100}x{580}")
        self.state("zoomed")

        # формируем макет
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure((4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.grid_rowconfigure((6), weight=1)

        # формируем заголовок
        self.heading = customtkinter.CTkLabel(self, text=msg.HEADING_LABEL, font=("Arial", 24, "bold"))
        self.heading.grid(row=0, column=0, columnspan=4, pady=(10, 20), padx=(20, 30), sticky="w")

        # формируем радиокнопки
        self.encoding_direction = tkinter.StringVar(value="encode")
        self.encoding_btn = customtkinter.CTkRadioButton(self, variable=self.encoding_direction, text=msg.ENCODING_LABEL, value="encode")
        self.encoding_btn.grid(row=1, column=0, padx=20, sticky="w")
        self.decoding_btn = customtkinter.CTkRadioButton(self, variable=self.encoding_direction, text=msg.DECODING_LABEL, value="decode")
        self.decoding_btn.grid(row=1, column=1, padx=20, sticky="w")

        # формируем поле с путем для файла
        self.path_input_label = customtkinter.CTkLabel(self, text=msg.CHOOSE_FILE_LABEL)
        self.path_input_label.grid(row=2, column=0, columnspan=4, pady=(5, 0), padx=(20, 30), sticky="w")
        self.path_input = customtkinter.CTkEntry(self, placeholder_text=msg.CHOOSE_FILE_PLACEHOLDER, state="readonly", width=500, corner_radius=0)
        self.path_input.grid(row=3, column=0, columnspan=3, padx=(20, 0), pady=(0, 5), sticky="nsew")
        self.path_input_button = customtkinter.CTkButton(self, text=msg.CHOOSE_FILE_BUTTON_LABEL, width=50, corner_radius=0, command=self.on_choose_file_button_press)
        self.path_input_button.grid(row=3, column=3, padx=(0, 30), pady=(0, 5), sticky="nsew")

        # формируем дроплист с выбором метода кодирования
        self.encoding_method = tkinter.StringVar(value="LZ77")
        self.coding_dropdown_label = customtkinter.CTkLabel(self, text=msg.CHOOSE_ENCODING_METHOD_LABEL)
        self.coding_dropdown_label.grid(row=4, column=0, columnspan=4, padx=(20, 30), pady=(5, 0), sticky="w")
        self.coding_dropdown = customtkinter.CTkOptionMenu(self, variable=self.encoding_method, values=["LZ77", "LZ78", "LZW"], corner_radius=0)
        self.coding_dropdown.grid(row=5, column=0, columnspan=4, padx=(20, 30), pady=(0, 5), sticky="nsew")

        # формируем кнопку действия
        self.action_button = customtkinter.CTkButton(self, text=msg.ACTION_BUTTON_LABEL, command=self.on_action_button_press, corner_radius=0, state="disabled")
        self.action_button.grid(row=6, column=2, columnspan=2, padx=(20, 30), pady=(15, 0), sticky="ne")

        # формируем макет с данными о результатах кодирования
        self.data_frame = customtkinter.CTkFrame(self, corner_radius=0, height=100)
        self.data_frame.grid_columnconfigure((0, 1), weight=1)
        self.data_frame.grid_rowconfigure((0, 1, 2), weight=0)
        self.data_frame.grid(row=0, column=4, rowspan=3, sticky="nsew")
        self.data_time_label = customtkinter.CTkLabel(self.data_frame, text=msg.ELAPSED_TIME_LABEL + "-")
        self.data_time_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        self.data_size_before_label = customtkinter.CTkLabel(self.data_frame, text=msg.SOURCE_TEXT_SIZE_LABEL + "-")
        self.data_size_before_label.grid(row=1, column=0, padx=20, sticky="w")
        self.data_size_after_label = customtkinter.CTkLabel(self.data_frame, text=msg.PROCESSED_TEXT_SIZE_LABEL + "-")
        self.data_size_after_label.grid(row=2, column=0, padx=20, sticky="w")

        # формируем кнопку сохранения результатов кодирования в файл
        self.save_button = customtkinter.CTkButton(self.data_frame, state="disabled", command=self.on_save_button_press, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Сохранить в файл", corner_radius=0)
        self.save_button.grid(row=0, column=1, rowspan=3, padx=20, pady=(20, 0), sticky="ne")

        # формируем текстовое поле для вывода данных
        self.textbox = customtkinter.CTkTextbox(self, corner_radius=0, state="disabled")
        self.textbox.grid(row=3, column=4, rowspan=4, sticky="nsew")

    # метод обработки нажания на кнопку выбора файла
    def on_choose_file_button_press (self):
        # получаем путь к файлу путем выбора из файловой системы
        filename = tkinter.filedialog.askopenfilename()

        # если файл выбран то запоминаем путь и активируем кнопку выполнить
        if filename:
            self.read_filename = filename
            self.path_input.configure(textvariable=tkinter.StringVar(value=filename))
            self.action_button.configure(state="normal")
    
    # метод обработки нажания на кнопку выполнить
    def on_action_button_press (self):
        # пытаемся выполнить кодирование
        try:
            # октрываем выбранный файл
            file = open(self.read_filename, "r", encoding="utf-8")

            # получаем текст из файла
            source_text = file.read()

            # закрываем файл
            file.close()

            # получаем выбранное направление кодирования
            encoding_direction = self.encoding_direction.get()

            # получаем выбранный метод кодирования
            encoding_method = self.encoding_method.get()

            # запоминаем время начала операции
            start_time = time.time()

            # выполняем условное ветвление для выбора метода кодирования
            if encoding_direction == "encode":
                if encoding_method == "LZ77":
                    processed_text = lz77.encode(source_text)
                elif encoding_method == "LZ78":
                    processed_text = lz78.encode(source_text)
                elif encoding_method == "LZW":
                    processed_text = lzw.encode(source_text)
            elif encoding_direction == "decode":
                if encoding_method == "LZ77":
                    processed_text = lz77.decode(source_text)
                elif encoding_method == "LZ78":
                    processed_text = lz78.decode(source_text)
                elif encoding_method == "LZW":
                    processed_text = lzw.decode(source_text)
            
            # запоминаем время окончания операции
            end_time = time.time()

            # сохраняем имя файла для использования при сохранении
            self.save_filename = f'{encoding_direction}d_{encoding_method}'

            # переводим кнопку сохранить в активное состояние
            self.save_button.configure(state="normal")

            # отображаем результат вычислений
            self.render_result({
                "source_text_length": len(source_text),
                "processed_text_length": len(processed_text),
                "processed_text": processed_text,
                "elapsed_time": end_time - start_time
            })
        # при возниконовении ошибок при попытке кодирования
        except Exception as exception:
            # выводим в консоль тип ошибки
            print(type(exception))

            # переводим кнопку сохранить в выключенное состояние
            self.save_button.configure(state="disabled")

            # устанавливаем текст ошибки в текстовое поле
            self.set_textbox_value(msg.ENCODE_ERROR_MESSAGE)

    # метод отрисовки результатов вычисления
    def render_result (self, data):
        # устанавливаем текст в текстовое поле
        self.set_textbox_value(data["processed_text"])

        # устанавливаем результаты вычислений в текстовые узлы
        self.data_time_label.configure(text=msg.ELAPSED_TIME_LABEL + str(data["elapsed_time"]))
        self.data_size_before_label.configure(text=msg.SOURCE_TEXT_SIZE_LABEL + str(data["source_text_length"]))
        self.data_size_after_label.configure(text=msg.PROCESSED_TEXT_SIZE_LABEL + str(data["processed_text_length"]))

    # метод обновления текста в текстовом поле
    def set_textbox_value (self, text):
        # переводим текстовое поле в обычное состояние
        self.textbox.configure(state="normal")

        # очищаем текстовое поле
        self.textbox.delete("1.0", "end")

        # устанавливаем новый текст в текстовое поле
        self.textbox.insert("0.0", text)

        # переводим текстовое поле в выключенное состояние
        self.textbox.configure(state="disabled")

    # метод обработки нажатия на кнопку сохранить
    def on_save_button_press (self):
        # получаем значение текстового поля
        text = self.textbox.get("1.0", "end-1c")

        # выбираем название файла для сохранения
        filename = tkinter.filedialog.asksaveasfilename(defaultextension="txt", initialfile = self.save_filename)

        # открываем выбранный файл
        file = open(filename, "w", encoding="utf-8")

        # запиываем значение
        file.write(text)

        # закрываем файл
        file.close()
