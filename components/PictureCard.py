import dash_mantine_components as dmc


def create_picture_card(image):
    card = dmc.Card(
        children = [
            dmc.CardSection(
                dmc.Image(
                    src=image["image_url"],
                    alt=image["species"],
                    style={"width": "100%", "height": "auto"}
                )
            ),
            dmc.CardSection(
                dmc.Flex(
                    direction="column",
                    justify="center",
                    align="center",
                    style={"height": "100%"},
                    children=[
                        dmc.Text(
                            image["species"].replace('-', ' ').capitalize(),
                            fw=500,
                            p="sm"
                        ),
                    ]
                )
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        p="md"
    )

    return card
