import pytest
import spacy

from main import parse_row


nlp = spacy.load('en_core_web_sm')
spacy.tokens.Token.set_extension('protected', default=False)


@pytest.mark.parametrize('data_in, data_out', [
    # pos
    ('I am a developer', 'I Am a Developer'),
    ('He is a student', 'He Is a Student'),
    ('Kyiv is the capital of Ukraine', 'Kyiv Is the Capital of Ukraine'),
    ('Jane reads a lot', 'Jane Reads a Lot'),
    ('Jane took a green book', 'Jane Took a Green Book'),
    ("It's too late", "It's Too Late"),

    # sub conjunctions
    ("Do as you want", "Do As You Want"),
    ("How to use a Macbook as a table", "How to Use a Macbook as a Table"),
    ("You and me", "You and Me"),

    # first word in the sentence
    ('I have found the book', 'I Have Found the Book'),
    ('the book was lost', 'The Book Was Lost'),
    ('as a table', 'As a Table'),
    ('111', '111'),
    ('#elise is a computer', '#Elise Is a Computer'),
    ('@elise is a computer', '@Elise Is a Computer'),

    # last word in the sentence
    ('come on', 'Come On'),
    ('111', '111'),
    ('take this', 'Take This'),
    ('this is the 1st', 'This Is the 1st'),
    ('this is the 1', 'This Is the 1'),
    ('this is the @first', 'This Is the @First'),

    # with a hyphen
    ('2011-2012 NHL team preview: Detroit Red Wings', '2011-2012 NHL Team Preview: Detroit Red Wings') ,
    ('Cal coach Jeff Tedford taking a different approach in 2010 -- Part 1', 'Cal Coach Jeff Tedford Taking a Different Approach in 2010 -- Part 1'),
    ('NU Hosts Illinois in First Nationally Televised Network Game at Welsh-Ryan', 'NU Hosts Illinois in First Nationally Televised Network Game at Welsh-Ryan'),
    ('Back to school, gluten-free style', 'Back to School, Gluten-Free Style'),
    ('free in-flight wi-fi', 'Free In-Flight Wi-Fi'),
    ('DIY pampering with Spa-in-a-basket', 'DIY Pampering with Spa-In-A-Basket'),
    ('and I saw what-the-strange-is-this thing', 'And I Saw What-The-Strange-Is-This Thing'),
    ('and I saw what-the-strange-is-this', 'And I Saw What-The-Strange-Is-This'),
    ('and I saw what-the-strange-is-', 'And I Saw What-The-Strange-Is-'),

    # additional
    ('Just BEcause happy hour for Canvas Art Program', 'Just because Happy Hour for Canvas Art Program'),
    ('The importance of eBay feedback', 'The Importance of eBay Feedback'),
    ("Ain't Misbehavin' next at the Crossroads Theatre Company", "Ain't Misbehavin' Next at the Crossroads Theatre Company"),
    ("I can't", "I Can't"),
    ("BREAKING: BP CEO Sold Shares of His Company's Stock Weeks before Gulf Disaster", "Breaking: BP CEO Sold Shares of His Company's Stock Weeks before Gulf Disaster")
])
def test_parser(data_in, data_out):
    assert parse_row(nlp, data_in) == data_out