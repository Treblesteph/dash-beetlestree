import dash_mantine_components as dmc

def create_header(logo):
    header = dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Tooltip(
                    id="burger-tooltip",
                    label="Click to see images!",
                    position="bottom",
                    color="orange.6",
                    withArrow=True,
                    opened=False,
                    hiddenFrom="sm",
                    children=dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                ),
                dmc.Image(src=logo, style={"height": "40px", "width": "auto"}),
                dmc.Title(
                    "Beetles Tree of Life",
                    c="teal.9",
                    size={"base": "lg", "sm": "xl", "md": "xl", "lg": "2xl"},
                )
            ],
            h="100%",
            px="md",
        )
    )
    return header
