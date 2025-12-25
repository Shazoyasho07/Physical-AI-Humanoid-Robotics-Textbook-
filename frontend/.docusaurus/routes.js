import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs/',
    component: ComponentCreator('/docs/', 'df9'),
    routes: [
      {
        path: '/docs/',
        component: ComponentCreator('/docs/', 'c0d'),
        routes: [
          {
            path: '/docs/',
            component: ComponentCreator('/docs/', 'a15'),
            routes: [
              {
                path: '/docs/basics/',
                component: ComponentCreator('/docs/basics/', '5cf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/capstone/',
                component: ComponentCreator('/docs/capstone/', 'c5b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro/',
                component: ComponentCreator('/docs/intro/', 'e44'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2/',
                component: ComponentCreator('/docs/ros2/', 'fc7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/simulation/',
                component: ComponentCreator('/docs/simulation/', 'baa'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla/',
                component: ComponentCreator('/docs/vla/', '2fc'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
