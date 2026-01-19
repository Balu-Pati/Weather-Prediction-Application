from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import FavoriteCity
from .extensions import db
from .weather import get_weather_data

main = Blueprint('main', __name__)


def _get_favorite_weather():
    favorite_cities = FavoriteCity.query.filter_by(user_id=current_user.id).all()
    return [get_weather_data(city.city_name) for city in favorite_cities]


@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    weather = None

    if request.method == 'POST':
        city_name = request.form.get('city')
        if city_name:
            weather = get_weather_data(city_name)
            if weather is None:
                flash("City not found. Please try again.", "danger")
            return render_template(
                'index.html',
                weather=weather,
                favorite_cities=_get_favorite_weather()
            )
    city_name = request.args.get('search')
    if city_name:
        weather = get_weather_data(city_name)

    return render_template(
        'index.html',
        weather=weather,
        favorite_cities=_get_favorite_weather()
    )


@main.route('/add_favorite', methods=['POST'])
@login_required
def add_favorite():
    city_name = request.form.get('city_name')

    if not city_name:
        flash("City name is required!", "danger")
        return redirect(url_for('main.home'))

    existing_fav = FavoriteCity.query.filter_by(user_id=current_user.id, city_name=city_name).first()
    if existing_fav:
        flash(f"{city_name} is already in your favorites!", "warning")
        return redirect(url_for('main.home', search=city_name))

    fav_count = FavoriteCity.query.filter_by(user_id=current_user.id).count()
    if fav_count >= 3:
        flash("You can only have up to 3 favorite cities.", "warning")
        return redirect(url_for('main.home', search=city_name))

    new_fav = FavoriteCity(user_id=current_user.id, city_name=city_name)
    db.session.add(new_fav)
    db.session.commit()

    flash(f"{city_name} added to favorites!", "success")
    return redirect(url_for('main.home', search=city_name))


@main.route('/delete_favorite/<string:name>', methods=['POST'])
@login_required
def delete_favorite(name):
    favorite = FavoriteCity.query.filter_by(city_name=name, user_id=current_user.id).first_or_404()

    db.session.delete(favorite)
    db.session.commit()

    flash("City removed from favorites!", "success")
    return redirect(url_for('main.home'))
