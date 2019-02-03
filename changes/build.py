Added the following if statement:
 'if skipped_images:
          for image in self.images:
              if image.name in skipped_images:
                  image.status = STATUS_UNMATCHED', for comptability reasons ("'NoneType' object is not iterable").
