from flask import render_template, request, current_app, Blueprint
from . import recommendations_logic_vol2 # veya projenin yapısına göre import yolunu düzenleyin

# Flask 2.0 ve sonrası için 'current_app' kullanmak daha iyidir
from flask import current_app as app

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/quiz')
def quiz():
    questions = current_app.config['QUIZ_QUESTIONS']
    return render_template('quiz_form_vol2.html', questions=questions)


@main.route('/result', methods=['POST'])
def result():
    quiz_questions = current_app.config['QUIZ_QUESTIONS']
    reader_type_genres = current_app.config['READER_TYPE_GENRES']
    scores = {ptype: 0 for ptype in reader_type_genres.keys()}

    for q in quiz_questions:
        qid = str(q['id'])
        if q.get("multiple"):
            selected_indices = request.form.getlist(f"question_{qid}")
            if "max_select" in q and len(selected_indices) > q["max_select"]:
                selected_indices = selected_indices[:q["max_select"]]

            for idx_str in selected_indices:
                try:
                    idx = int(idx_str)
                    if 0 <= idx < len(q['options']):
                        option = q['options'][idx]
                        for ptype in option['types']:
                            if ptype in scores:
                                scores[ptype] += 1
                except ValueError:
                    pass
        else:
            selected_idx_str = request.form.get(f"question_{qid}")
            if selected_idx_str is not None:
                try:
                    idx = int(selected_idx_str)
                    if 0 <= idx < len(q['options']):
                        option = q['options'][idx]
                        for ptype in option['types']:
                            if ptype in scores:
                                scores[ptype] += 1
                except ValueError:
                    pass

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]

    return render_template('quiz_result.html', top_types=top_3, reader_type_genres_keys=reader_type_genres.keys())

@main.route('/recommendations')
def recommendations():
    user_reader_type = request.args.get('type')
    reader_type_genres = current_app.config['READER_TYPE_GENRES']
    global_excluded_tags = current_app.config['GLOBAL_EXCLUDED_TAGS']
    character_specific_exclusions = current_app.config['CHARACTER_SPECIFIC_EXCLUSIONS']
    tag_weights = current_app.config['TAG_WEIGHTS']
    if not user_reader_type or user_reader_type not in reader_type_genres:
        return "Geçersiz okuyucu tipi veya tip belirtilmedi. <a href='/'>Ana Sayfa</a>"

    preferred_genres = reader_type_genres[user_reader_type]

    # Genel ve özel dışlama listelerini birleştir
    final_excluded_tags = set(global_excluded_tags)
    specific_exclusions = character_specific_exclusions.get(user_reader_type, [])
    final_excluded_tags.update(specific_exclusions)

    # O karaktere özel ağırlıkları al
    character_weights = tag_weights.get(user_reader_type, {})

    # Nihai fonksiyonu çağır (api_key parametresi OLMADAN)
    recommended_books = recommendations_logic_vol2.get_recommendations_with_weighted_scoring(
        preferred_genres,
        final_limit=12,
        excluded_tags=list(final_excluded_tags),
        tag_weights=character_weights
    )

    return render_template('recommendations.html', reader_type=user_reader_type, books=recommended_books)