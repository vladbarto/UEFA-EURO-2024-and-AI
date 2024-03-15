def construct_table(data, categories):
    # simple dynamically created table to show pulled dataset
    # prints in here will only show in the console, not on the website -> debugging
    # print("data:", data)
    # print("categories:", categories)
    content = """
    <table class="table table-hover">
        <thead>
        <tr>
            <th scope="col">#</th>
    """
    # get category data
    for i in range(0, len(categories)):
        content += """<th scope="col">"""
        content += str(categories[i])
        content += """</th>"""
    content += """
        </tr>
        </thead>
        <tbody>
        """
    # get main data
    # print(len(data))
    # print(len(data[0]))
    for i in range(0, len(data)):
        content += """<tr>"""
        content += """<th scope="row">""" + str(i) + """</th>"""
        for k in range(0, len(data[0])):
            content += """<td>""" + str(data[i][k]) + """</td>"""
        content += """</tr>"""
    content += """
        </tbody>
    </table>"""
    print("render finished")
    # print(content)
    return content


def construct_prediction(prediction: str):
    content = """
        <button class="prediction-label">
        """
    content += """<p>""" + prediction + """</p>"""

    content += """</button>"""
    print("render finished")
    return content


def construct_button(country_name: str):
    content = f"""
        <a href="/moreabout/{country_name}">
            <button class="redirect-country">
                {country_name}
            </button>
        </a>
    """
    return content



def construct_list(lst: list):
    content = ""
    for row in lst:
        content += construct_button(row)
    return content


def construct_match_card(info: list, repetitive_team: str):
    content = """
        <div class="match-card-co">
        """
    content += """
        <div class="time-and-venue-co">
        <p>
        """
    content += info[1] + ", " + info[0] + "</p>"
    content += "<p>"
    content += info[2] + "</p></div>"
    content += """
        <div class="match-teams">
        """
    content += "<p>" + repetitive_team + "</p><p>" + info[3] + "</p>"
    content += "</div></div>"
    return content
