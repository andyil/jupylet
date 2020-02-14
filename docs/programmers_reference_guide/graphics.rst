PROGRAMMING GRAPHICS
====================

Hello, Jupylet!
---------------

We begin with the simplest *Jupylet* app. It displays a scolling banner with the
text *"hello, world"*. You can find the notebook at
`examples/hello-jupylet.ipynb <https://github.com/nir/jupylet/blob/master/examples/hello-jupylet.ipynb>`_.

.. note::
    To understand this code you need to understand Python
    `imports <https://docs.python.org/3.7/tutorial/modules.html#modules>`_,
    `functions <https://docs.python.org/3.7/tutorial/controlflow.html#defining-functions>`_
    , and `classes <https://docs.python.org/3.7/tutorial/classes.html>`_.

The code begins with two import statements that import the
:class:`jupylet.app.App` class which represents a game or an application and
the `Label` class which will be used to display the text:

.. code-block:: python

    from jupylet.label import Label
    from jupylet.app import App

Next, we instantiate the application object and specify the width and height
of the game canvas:

.. code-block:: python

    app = App(width=320, height=64)

Then we instantiate a label with the text *hello, world*:

.. code-block:: python

    hello = Label('hello, world', color='cyan', font_size=32, x=app.width, y=16)

There are two things to note here:

- By default, the *x* and *y* coordinates of a label correspond to its lower
  left corner. By setting the initial *x* position to *app.width* we
  effectively position the label just outside the right hand side of the
  application canvas.

- The label color can be any of names defined by the `W3C SVG standard <https://www.w3.org/TR/SVG11/types.html#ColorKeywords>`_
  or it can be any RGB color of the form '#abcdef' - see here `<https://www.color-hex.com/>`_.

.. code-block:: python

    @app.event
    def on_draw():
        app.window.clear()
        hello.draw()

    @app.run_me_again_and_again(1/30)
    def scroll(dt):
        hello.x -= 1
        if hello.x < -220:
            hello.x = app.width

    app.run()

If you run the notebook a canvas will appear with the following animation:

.. image:: ../images/hello-world.gif


