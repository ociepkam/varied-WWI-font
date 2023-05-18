#!/usr/bin/env python
# -*- coding: utf8 -*

import random
from psychopy import visual

stim_text = {'CZERWONY': 'red', 'NIEBIESKI': '#5e75d9', 'BRAZOWY': '#574400', 'ZIELONY': 'green'}  # text: color
stim_neutral = "HHHHHHHH"
stim_distractor = ['WYSOKA', 'UKRYTA', u'GŁĘBOKA', 'DALEKA']

colors_text = list(stim_text.keys())
random.shuffle(colors_text)
colors_names = [stim_text[color] for color in colors_text]
left_hand = colors_text[:2]
right_hand = colors_text[2:]

last_color = None


def prepare_trial(trial_type, win, text_height, words_dist):
    global last_color

    if trial_type == 'trial_con_con_con':
        possible_text = list(stim_text.keys())
        if last_color is not None:
            possible_text.remove([k for k, v in stim_text.items() if v == last_color][0])
        text = random.choice(possible_text)
        color = stim_text[text]
        words = [text, text, text]

    elif trial_type == 'trial_inc1_inc1_inc1':
        text = random.choice(list(stim_text.keys()))
        if text in left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        words = [text, text, text]

    elif trial_type == 'trial_inc1_inc2_inc1':
        possible_colors = [stim_text[key] for key in stim_text]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        possible_words = [key for key in stim_text if stim_text[key] != color]
        random.shuffle(possible_words)
        words = [possible_words[0], possible_words[1], possible_words[0]]

    elif trial_type == 'trial_inc1_inc2_inc3':
        possible_colors = [stim_text[key] for key in stim_text]
        if last_color in possible_colors:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)
        words = [key for key in stim_text if stim_text[key] != color]
        random.shuffle(words)

    elif trial_type == 'trial_neu_neu_neu':
        words = [stim_neutral, stim_neutral, stim_neutral]
        possible_colors = list(stim_text.values())
        if last_color is not None:
            possible_colors.remove(last_color)
        color = random.choice(possible_colors)

    else:
        raise Exception('Wrong trigger type')

    last_color = color

    stim1 = visual.TextStim(win, color=color, text=words[0], height=text_height, pos=(0, words_dist))
    stim2 = visual.TextStim(win, color=color, text=words[1].lower(), height=text_height, pos=(0, 0))
    stim3 = visual.TextStim(win, color=color, text=words[2].lower(), height=text_height, pos=(0, -words_dist), italic=True)
    # print({'trial_type': trial_type, 'text': words, 'color': color, 'stim': [stim1, stim2, stim3]})
    return {'trial_type': trial_type, 'text': words, 'color': color, 'stim': [stim1, stim2, stim3]}


def prepare_part(trials_con_con_con, trials_inc1_inc1_inc1, trials_inc1_inc2_inc1, trials_inc1_inc2_inc3,
                 trials_neu_neu_neu, win, text_height, words_dist):
    trials = ['trial_con_con_con'] * trials_con_con_con + \
             ['trial_inc1_inc1_inc1'] * trials_inc1_inc1_inc1 + \
             ['trial_inc1_inc2_inc1'] * trials_inc1_inc2_inc1 + \
             ['trial_inc1_inc2_inc3'] * trials_inc1_inc2_inc3 + \
             ['trial_neu_neu_neu'] * trials_neu_neu_neu
    random.shuffle(trials)
    return [prepare_trial(trial_type, win, text_height, words_dist) for trial_type in trials]


def prepare_exp(data, win, text_size, words_dist):
    text_height = 1.5 * text_size
    training1_trials = prepare_part(data['Training1_trials_con_con_con'],
                                    data['Training1_trials_inc1_inc1_inc1'],
                                    data['Training1_trials_inc1_inc2_inc1'],
                                    data['Training1_trials_inc1_inc2_inc3'],
                                    data['Training1_trials_neu_neu_neu'],
                                    win, text_height, words_dist)

    training2_trials = prepare_part(data['Training2_trials_con_con_con'],
                                    data['Training2_trials_inc1_inc1_inc1'],
                                    data['Training2_trials_inc1_inc2_inc1'],
                                    data['Training2_trials_inc1_inc2_inc3'],
                                    data['Training2_trials_neu_neu_neu'],
                                    win, text_height, words_dist)

    experiment_trials = prepare_part(data['Experiment_trials_con_con_con'],
                                     data['Experiment_trials_inc1_inc1_inc1'],
                                     data['Experiment_trials_inc1_inc2_inc1'],
                                     data['Experiment_trials_inc1_inc2_inc3'],
                                     data['Experiment_trials_neu_neu_neu'],
                                     win, text_height, words_dist)

    return [training1_trials, training2_trials], experiment_trials, colors_text, colors_names
