"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'melon-secrets'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types

    # FIRST VERSION
    # melons_only.pop('_flash')
    # melons_only = session.keys()
    # cart = {}    
    # for i in melons_only:
    #     print "this is i:", session[i], i
    #     melon_quantity = session[i]
    #     melon_name = this_melon.common_name
    #     melon_price = this_melon.price
    #     melon_total = melon_price * melon_quantity

    melons_in_cart = {}



    for item in session['cart']:
        if item in melons_in_cart.keys():
            melons_in_cart[item]['quantity'] += 1
        else:
            this_melon = melons.get_by_id(item)
            melons_in_cart.setdefault(item, {})
            melons_in_cart[item].setdefault('quantity', 1)
            melons_in_cart[item]['name'] = this_melon.common_name
            melons_in_cart[item]['price'] = this_melon.price
        
        melons_in_cart[item]['total'] = (melons_in_cart[item]['price'] *
                                        melons_in_cart[item]['quantity'])

    super_total = 0
    for item in melons_in_cart.keys():
        super_total += melons_in_cart[item]['total']

    # print "*** THIS IS OUR CART ****", melons_in_cart



    return render_template("cart.html", cart = melons_in_cart, 
                            super_total = super_total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session

    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(id)

    # FIRST VERSION
    # if session.get(id, 0) == 0:
    #     session[id] = 1
    # else:
    #     session[id]+= 1
        

    # print session

    flash("Melon was successfully added to cart.")
    # session.setdefault(id, 0) += 1

    return redirect("/cart")



@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!
    user_email =  request.form.get('email')
    user_pw = request.form.get('password')
    try:
        user = customers.get_by_email(user_email)
        if user_pw == user.password:
            # log them in
            flash("You are logged in.")
            # redirect to /melons
        else:
            flash("Incorrect password.")
            #redirect to login page
    except KeyError:
        flash("User not found! Please create account.")
    

    # return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
