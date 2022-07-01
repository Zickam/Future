import json, os
import pickle

config_loc = os.path.join(os.getcwd(), "Config")

dev_config = "dev_config.txt"
custom_config = "custom_config.txt"
legit_config = "legit_config.txt"
rage_config = "rage_config.txt"
semi_config = "semi_config.txt"

def LoadConfig(name):

    if name == "Custom":
        file_to_read_to = open(os.path.join(config_loc, custom_config), "rb")
        config = pickle.load(file_to_read_to)

    elif name == "Legit":
        file_to_read_to = open(os.path.join(config_loc, legit_config), "rb")
        config = pickle.load(file_to_read_to)

    elif name == "Rage":
        file_to_read_to = open(os.path.join(config_loc, rage_config), "rb")
        config = pickle.load(file_to_read_to)

    elif name == "Semi":
        file_to_read_to = open(os.path.join(config_loc, semi_config), "rb")
        config = pickle.load(file_to_read_to)

    elif name == "Dev":
        file_to_read_to = open(os.path.join(config_loc, dev_config), "rb")
        config = pickle.load(file_to_read_to)

    return config

def SaveConfig(buttons, name):

    config_to_dump = dict()

    def iterateThroughButtonDependencies(object_name, object_dependencies):

        objects = dict()

        for _object_name, object_props in object_dependencies.items():
            _object = object_props[0]
            dependencies = object_props[1]
            object_type = type(_object).__name__

            if object_type == "ConfigSaver":
                continue

            iterated_dependencies = None
            if hasattr(_object, "Tab"):
                if dependencies != None:
                    iterated_dependencies = iterateThroughButtonDependencies(_object_name, dependencies)

            if object_type == "Button":
                _object_state = _object.State
                objects[_object_name] = [["State", _object_state], iterated_dependencies]

            elif object_type == "Selector":
                _object_array = _object.array
                _object_selected = _object.selected
                objects[_object_name] = [["selected", _object_array, _object_selected], iterated_dependencies]

            elif object_type == "ColorPicker":
                _object_state = _object.processedcolor
                objects[_object_name] = [["processedcolor", _object_state], iterated_dependencies]

            elif object_type == "Slider":
                _object_state = _object.State
                objects[_object_name] = [["VisualState", _object_state], iterated_dependencies]

            elif object_type == "Textbox":
                _object_state = _object.user_text
                objects[_object_name] = [["user_text", _object_state], iterated_dependencies]

            elif object_type == "Searchbox":
                _object_state = _object.text
                objects[_object_name] = [["text", _object_state], iterated_dependencies]

            elif object_type == "Checkbox":
                _object_state = _object.clicked
                objects[_object_name] = [["clicked", _object_state], iterated_dependencies]

        return objects

    for object_name, object_props in buttons.items():
        _object = object_props[0]
        dependencies = object_props[1]

        object_type = type(_object).__name__

        iterated_dependencies = None

        if hasattr(_object, "Tab"):
            if dependencies != None:
                iterated_dependencies = iterateThroughButtonDependencies(object_name, dependencies)

        if object_type == "Button":
            _object_state = _object.State
            config_to_dump[object_name] = [["State", _object_state], iterated_dependencies]

        elif object_type == "Selector":
            _object_array = _object.array
            _object_selected = _object.selected
            config_to_dump[object_name] = [["selected", _object_array, _object_selected], iterated_dependencies]

        elif object_type == "ColorPicker":
            _object_state = _object.processedcolor
            config_to_dump[object_name] = [["processedcolor", _object_state], iterated_dependencies]

        elif object_type == "Slider":
            _object_state = _object.VisualState
            config_to_dump[object_name] = [["VisualState", _object_state], iterated_dependencies]

        elif object_type == "Textbox":
            _object_state = _object.user_text
            config_to_dump[object_name] = [["user_text", _object_state], iterated_dependencies]

        elif object_type == "Searchbox":
            _object_state = _object.text
            config_to_dump[object_name] = [["text", _object_state], iterated_dependencies]

        elif object_type == "Checkbox":
            _object_state = _object.clicked
            config_to_dump[object_name] = [["clicked", _object_state], iterated_dependencies]

    if name == "Custom":
        with open(os.path.join(config_loc, custom_config), "wb") as file:
            pickle.dump(config_to_dump, file)

    elif name == "Rage":
        with open(os.path.join(config_loc, rage_config), "wb") as file:
            pickle.dump(config_to_dump, file)

    elif name == "Legit":
        with open(os.path.join(config_loc, legit_config), "wb") as file:
            pickle.dump(config_to_dump, file)

    elif name == "Semi":
        with open(os.path.join(config_loc, semi_config), "wb") as file:
            pickle.dump(config_to_dump, file)

    elif name == "Dev":
        with open(os.path.join(config_loc, dev_config), "wb") as file:
            pickle.dump(config_to_dump, file)

