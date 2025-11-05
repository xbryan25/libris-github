export default defineAppConfig({
  ui: {
    colors: {
      primary: 'green',
      neutral: 'zinc'
    },
    skeleton: {
      base: 'animate-pulse rounded-md bg-elevated'
    },
    fileUpload: {
      compoundVariants: [
        {
          layout: 'grid',
          multiple: true,
          class: {
            files: 'grid grid-cols-2 md:grid-cols-5 gap-4 w-full',
            file: 'p-0 aspect-square'
          }
        },
        {
          layout: 'grid',
          multiple: false,
          class: {
            file: 'absolute inset-0 p-0'
          }
        },
      ],
    }
  }   
})