
export const deviceSizes = {
    minMobile: '320',
    minTablet: '481',
    minLaptop: '769',
    minDesktop: '1025',
    xlScreens: '1201',
    xxlScreens: '1401'
};

export const breakPoints = {
    mobile: `(min-width: ${deviceSizes.minMobile}px)`,
    tablet: `(min-width: ${deviceSizes.minTablet}px)`,
    laptop: `(min-width: ${deviceSizes.minLaptop}px)`,
    desktop: `(min-width: ${deviceSizes.minDesktop}px)`,
};