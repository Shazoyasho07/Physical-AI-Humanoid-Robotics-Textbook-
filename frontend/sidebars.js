// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapters',
      items: [
        'basics',
        'ros2',
        'simulation',
        'vla',
        'capstone',
      ],
    },
  ],
};

module.exports = sidebars;