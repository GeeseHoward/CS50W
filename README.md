# Project 0

**Web Programming with Python and JavaScript**

**Overview**

This website is kind of like a personal blog. It has 6 sections:

1) Homepage/index.html (just contains a paragraph)
2) Likes/things_i_like.html (Contains an ordered list)
3) Dislikes/things_i_dont_like.html (Contains an unordered list)
4) Aliens/aliens.html (Contains a bootstrap table component, images, its own css/scss with media queries, sass variables and inheritance)
5) About me/about_me.html (Contains just paragraphs)
6) Contact/contact.html (Contains a bootstrap form component)

The main project has a common css file (common.css) and a common scripts file (common.js) which is included in all pages.

The purpose of common.js is to include all the headers/html etc that are common to all files. For example since the top navigation bar
is common to all pages, the common.js prepends it in the body. jQuery is used to accomplish this.

The most developed page is aliens.html. It has its own css (aliens.css/aliens.scss) which employ media queries, sass
variables and inheritance.

**Summary of where the requirements are located**:
* Ordered list (things_i_like.html)
* Unordered list (things_i_dont_like.html)
* Table (aliens.html)
* Media query (aliens.html/aliens.css/aliens.scss)
* Bootstrap 4
    * Bootstrap components
        * Navbar component is common to all pages (common_includes.html included using jQuery in common.js)
        * Form component located in contact.html
        * Table component located in aliens.html
    * Bootstrap grid
        * Images in aliens.html use grid model
* CSS Selectors used
    * Multiple element selector (aliens.css)
    * Descendant selector (aliens.css)
    * Child selector (common.css)
    * Psuedoelement selector (aliens.css)
    * Psuedoclass selector (common.css)
* SCSS
    * Variables, nesting and inheritance are used in aliens.scss