import pytest
from model import Question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_invalid_choices():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a'*201, False)
        
def test_answer_question():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    choice_a = question.choices[0]
    choice_b = question.choices[1]
    
    assert len(question.correct_selected_choices([choice_a.id])) == 0
    assert len(question.correct_selected_choices([choice_b.id])) == 1

def test_selecting_multiple_choices_when_invalid():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    choice_a = question.choices[0]
    choice_b = question.choices[1]
    
    with pytest.raises(Exception):
        question.correct_selected_choices([choice_a.id, choice_b.id])
    
def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    choice_a = question.choices[0]
    question.remove_choice_by_id(choice_a.id)
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    choice_a = question.choices[0]
    choice_b = question.choices[1]
    question.set_correct_choices([choice_a.id])

    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct
    assert len(question.correct_selected_choices([choice_a.id])) == 1
    assert len(question.correct_selected_choices([choice_b.id])) == 0
    
def test_correct_selected_choices_returns_only_right_answers():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', False) 
    question.add_choice('b', True)  
    
    result = question.correct_selected_choices([1, 2])
    assert result == [2]

def test_remove_invalid_choice_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    question.remove_choice_by_id(1)
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(1)

def test_remove_choice_from_empty_question():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(1)