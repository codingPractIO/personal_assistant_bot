from .nodes import (
    Root,
    Registration, Registration2, Registration3,
    MainScreen,
)
from core.nodes.nodes_constants import (
    CONSTRUCTOR,
    CHILDREN,
)


tree_config = {
    CONSTRUCTOR: Root,
    CHILDREN: [
        {
            CONSTRUCTOR: MainScreen,
            CHILDREN: [
            ],
        },
        {
            CONSTRUCTOR: Registration,
            CHILDREN: [
                {
                    CONSTRUCTOR: Registration2,
                    CHILDREN: [
                        {
                            CONSTRUCTOR: Registration3,
                        }
                    ]
                }
            ],
        },
    ],
}
