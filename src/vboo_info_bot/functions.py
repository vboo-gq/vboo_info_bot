"""Common functions"""

from telegram.utils.helpers import escape_markdown


def telegram_format_article(article):
    """Format article object for telegram"""
    title = '*[{}](https://m.rivalregions.com/#news/show/{})*'.format(
        escape_markdown(article['article_title'], 2),
        article['article_id'],
    )
    author = '[{}](https://m.rivalregions.com/#slide/profile/{})'.format(
        escape_markdown(article['author_name'], 2),
        article['author_id'],
    )
    underline = '{}, rating: {}, comments: {}'.format(
        escape_markdown(article['post_date'].strftime('%Y-%m-%d %H:%M'), 2),
        article['rating'],
        article['comments'],
    )
    if article['content_text'].strip():
        article_content = '_{}_'.format(escape_markdown(article['content_text'][0:144].strip(), 2))
    else:
        article_content = ''
    formatted_article = '{} by: {}\n{}\n{}'.format(
        title,
        author,
        underline,
        article_content,
    )
    return formatted_article

def abbreviate(string, max_lenght):
    """Abriviate string to only first letters"""
    if len(string) <= max_lenght:
        return string
    abbreviation = ''
    for word in string.split(' '):
        abbreviation += word[0:1].upper()
    return abbreviation

def format_state_region(side):
    """Format state and region name"""
    state = '*[{}](https://m.rivalregions.com/#state/details/{})*'.format(
        escape_markdown(abbreviate(side['state_name'], 4), 2),
        side['state_id'],
    )
    region = '[{}](http://m.rivalregions.com/#map/details/{})'.format(
        escape_markdown(side['region_name'], 2),
        side['region_id'],
    )
    return '{} {}'.format(state, region)

def roundk(integer):
    """Round down number"""
    thousand = 0
    decimal = 0
    while integer >= 999 or integer <= -999:
        thousand += 1
        decimal = int(str(integer)[-3:-2])
        integer = int(str(integer)[:-3])
    if decimal == 0:
        return '{}{}'.format(integer, 'k' * thousand)
    return '{}.{}{}'.format(integer, decimal, 'k' * thousand)



def telegram_format_war(war):
    """Format war object for article"""
    row_list = []
    if 'region_name' in war['attack']:
        row_list.append('{} vs {}'.format(
            format_state_region(war['attack']),
            format_state_region(war['defend'])
        ))
    else:
        row_list.append('{} vs {}'.format(
            '*{}*'.format(war['type']),
            format_state_region(war['defend'])
        ))

    total_damage = war['attack']['damage'] + war['defend']['damage']
    row_list.append('{} *vs* {} \\= {}'.format(
        escape_markdown('{} ({:0.2f}%)'.format(
            roundk(war['attack']['damage']),
            100 / total_damage * war['attack']['damage']
        ), 2),
        escape_markdown('{} ({:0.2f}%)'.format(
            roundk(war['defend']['damage']),
            100 / total_damage * war['defend']['damage']
        ), 2),
        escape_markdown(roundk(war['damage']), 2),
    ))

    row_list.append(
        'finish: {} UTC'.format(escape_markdown(war['finish_date'].strftime('%Y-%m-%d %H:%M'), 2))
    )

    if war['time_left']:
        row_list.append('time left: {}'.format(escape_markdown(str(war['time_left']))))
    else:
        row_list.append('max damage [{}](https://m.rivalregions.com/#slide/profile/{}): {}'.format(
            war['max_hero_name'],
            war['max_hero_id'],
            escape_markdown(roundk(war['max_hero_damage']), 2),
        ))

    row_list.append('{} \\| {}'.format(
        '[mobile](https://m.rivalregions.com/#war/details/{})'.format(war['war_id']),
        '[desktop](http://rivalregions.com/#war/details/{})'.format(war['war_id']),
    ))

    return '\n'.join(row_list)
