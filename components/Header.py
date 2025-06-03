import dash_mantine_components as dmc

def create_header(logo):
    header = dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                dmc.Image(src=logo, style={"height": "40px", "width": "auto"}),
                dmc.Title("Beetles Tree of Life", c="teal.9"),
            ],
            h="100%",
            px="md",
        )
    )
    return header
