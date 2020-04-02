class FriezeError(Exception):
    def __init__(self, message):
        self.message = message

class Frieze:
    def __init__(self, fName):
        self.frieze, self.period = self._check_valid_frieze(fName)
        self.fName = fName

    def _check_valid_frieze(self, fName):
        frieze = []
        with open(fName) as friezeFile:
            try:
                rowNum = 0
                for line in friezeFile:
                    if not line.isspace():
                        tempRow = [int(val) for val in line.split()]
                        for val in tempRow:
                            if val < 0 or val > 15:
                                raise FriezeError('Incorrect input.') # First check whether the input is all numbers form 0 to 15
                        frieze.append(tempRow)
                        if rowNum:
                            rowLength = len(frieze[rowNum])
                            if len(frieze[rowNum - 1]) != rowLength or rowLength < 5 or rowLength > 51:
                                raise FriezeError('Incorrect input.') # Then check whether the length of each row is equal and at least 4+1, at most 50+1
                        rowNum += 1
                if rowNum < 3 or rowNum > 17:
                    raise FriezeError('Incorrect input.') # Then check whether the height of frieze is at least 2+1, at most 16+1
            except ValueError:
                raise FriezeError('Incorrect input.')

        # Check whether the input is a frieze

        friezeLength = len(frieze[0]) - 1
        friezeHeight = len(frieze) - 1
        
        # First we need to check whether the boundary is correct
        # The representation in the first line except last one should not exceed boundary, and it should be a horizontal line
        for val in frieze[0][0:-1]:
            if val not in (4, 12):
                raise FriezeError('Input does not represent a frieze.')
        
        # The representation in the last column should not exceed boundary
        if frieze[0][-1]:
            raise FriezeError('Input does not represent a frieze.') # Only 0 will not exceed boundary
        for row in frieze[1:]:
            if row[-1] not in (0, 1):
                raise FriezeError('Input does not represent a frieze.') # Only 0 and 1 will not exceed boundary
            if row[-1]:
                if not row[0]%2:
                    raise FriezeError('Input does not represent a frieze.') # If the right boundary is not overlapping with the left boundary it is not a frieze

        # The representation in the last line should not exceed boundary, and it should be a horizontal line
        for val in frieze[-1][0:-1]:
            if val < 4 or val > 7:
                raise FriezeError('Input does not represent a frieze.') # The number > 7 will go southeast

        # Then we need to check whether the representation in the inner frieze contains a cross
        for i in range(friezeHeight):
            for j in range(friezeLength):
                if frieze[i][j] > 7:
                    if frieze[i+1][j] in (2, 3, 6, 7, 10, 11, 14, 15):
                        raise FriezeError('Input does not represent a frieze.') # If the number in the next line goes northeast it will contain a cross

        # Lastly we need to make sure it is a frieze and compute the period
        friezePeriod = None
        for period in range(1, friezeLength):
            is_transtive = True
            for i in range(friezeHeight + 1):
                if not is_transtive:
                        break
                for j in range(friezeLength):
                    if frieze[i][j] != frieze[i][(j + period) % (friezeLength)]:
                        is_transtive = False
                        break
            if is_transtive:
                friezePeriod = period
                break

        if friezePeriod is not None and friezePeriod > 1:
            return ([[(val, val >> 3, (val & 4) >> 2, (val & 2) >> 1, val & 1) for val in row] for row in frieze], friezePeriod)
        else:
            raise FriezeError('Input does not represent a frieze.')


    def analyse(self):
        vertical_reflection = self._check_vertical_reflection()
        horizontal_reflection = self._check_horizontal_reflection()
        glided_horizontal_reflection = self._check_glided_horizontal_reflection()
        rotation_reflection = self._check_rotation_reflection()
        
        if not vertical_reflection and not horizontal_reflection and not glided_horizontal_reflection and not rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation only.')
        elif vertical_reflection and not horizontal_reflection and not glided_horizontal_reflection and not rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and vertical reflection only.')
        elif not vertical_reflection and horizontal_reflection and not rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and horizontal reflection only.')
        elif not vertical_reflection and not horizontal_reflection and glided_horizontal_reflection and not rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and glided horizontal reflection only.')
        elif not vertical_reflection and not horizontal_reflection and not glided_horizontal_reflection and rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and rotation only.')
        elif vertical_reflection and not horizontal_reflection and glided_horizontal_reflection and rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        glided horizontal and vertical reflections, and rotation only.')
        elif vertical_reflection and horizontal_reflection and rotation_reflection:
            print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        horizontal and vertical reflections, and rotation only.')


    def _display_matrix(self, matrix):
        for row in matrix:
            for val in row:
                print(f'{val:3d}',end = '')
            print()

    def _check_vertical_reflection(self):
        friezeHeight = len(self.frieze)
        friezeLength = len(self.frieze[0]) - 1

        # First check whether the frieze is vertical reflection base on the axis on the nodes
        for axis in range(self.period + 1):
            is_reflective = True
            # check whether the nodes are reflective on the left and right side of the axis
            for y in range(self.period + 1):
                if not is_reflective:
                    break
                for x in range(friezeHeight):
                    # first check whether the right side of the axis is vertival reflection
                    if self.frieze[x][(axis+y)%friezeLength][4] and not self.frieze[x][(axis-y)%friezeLength][4]:
                        is_reflective = False
                        break
                    if self.frieze[x][(axis+y)%friezeLength][3] and not self.frieze[x-1][(axis-y-1)%friezeLength][1]: # since the nodes in first row won't point northeast, x-1 is safe
                        is_reflective = False
                        break
                    if self.frieze[x][(axis+y)%friezeLength][2] and not self.frieze[x][(axis-y-1)%friezeLength][2]:
                        is_reflective = False
                        break
                    if self.frieze[x][(axis+y)%friezeLength][1] and not self.frieze[x+1][(axis-y-1)%friezeLength][3]: # since the nodes in last row won't point southeast, x+1 is safe
                        is_reflective = False
                        break
                    # then check whether the left side of the axis is vertical reflection
                    if y > 0:
                        if self.frieze[x][(axis-y)%friezeLength][4] and not self.frieze[x][(axis+y)%friezeLength][4]:
                            is_reflective = False
                            break
                        if self.frieze[x][(axis-y)%friezeLength][3] and not self.frieze[x-1][(axis+y-1)%friezeLength][1]: # since the nodes in first row won't point northeast, x-1 is safe
                            is_reflective = False
                            break
                        if self.frieze[x][(axis-y)%friezeLength][2] and not self.frieze[x][(axis+y-1)%friezeLength][2]:
                            is_reflective = False
                            break
                        if self.frieze[x][(axis-y)%friezeLength][1] and not self.frieze[x+1][(axis+y-1)%friezeLength][3]: # since the nodes in last row won't point southeast, x+1 is safe
                            is_reflective = False
                            break
            if is_reflective:
                return True
            
        # Then check whether the frieze is vertical reflection between the nodes
        for axis in range(self.period + 1):
            is_reflective = True
            # First check whether the nodes on the axis is reflective and not contain nodes pointing northeeast and southeast
            # otherwise it would be a cross.
            for x in range(friezeHeight):
                if self.frieze[x][axis][4] and not self.frieze[x][(axis+1)%friezeLength][4]:
                    is_reflective = False
                    break
                if self.frieze[x][axis][3] or self.frieze[x][axis][1]:
                    is_reflective = False
                    break
            # Then check whether the nodes are reflective on the left and right side of the axis
            for y in range(1, self.period + 1):
                if not is_reflective:
                    break
                for x in range(friezeHeight):
                    # first check whether the right side of the axis is vertival reflection
                    if self.frieze[x][(axis+y)%friezeLength][4] and not self.frieze[x][(axis-y+1)%friezeLength][4]:
                        is_reflective = False
                        break
                    if self.frieze[x][(axis+y)%friezeLength][3] and not self.frieze[x-1][(axis-y)%friezeLength][1]: # since the nodes in first row won't point northeast, x-1 is safe
                        is_reflective = False
                        break
                    if self.frieze[x][(axis+y)%friezeLength][2] and not self.frieze[x][(axis-y)%friezeLength][2]:
                        is_reflective = False
                        break
                    if self.frieze[x][(axis+y)%friezeLength][1] and not self.frieze[x+1][(axis-y)%friezeLength][3]: # since the nodes in last row won't point southeast, x+1 is safe
                        is_reflective = False
                        break
                    # then check whether the left side of the axis is vertical reflection
                    if self.frieze[x][(axis-y)%friezeLength][4] and not self.frieze[x][(axis+y+1)%friezeLength][4]:
                        is_reflective = False
                        break
                    if self.frieze[x][(axis-y)%friezeLength][3] and not self.frieze[x-1][(axis+y)%friezeLength][1]: # since the nodes in first row won't point northeast, x-1 is safe
                        is_reflective = False
                        break
                    if self.frieze[x][(axis-y)%friezeLength][2] and not self.frieze[x][(axis+y)%friezeLength][2]:
                        is_reflective = False
                        break
                    if self.frieze[x][(axis-y)%friezeLength][1] and not self.frieze[x+1][(axis+y)%friezeLength][3]: # since the nodes in last row won't point southeast, x+1 is safe
                        is_reflective = False
                        break
            if is_reflective:
                return True
        return False

    def _check_horizontal_reflection(self):
        friezeHeight = len(self.frieze)
        friezeLength = len(self.frieze[0])

        # If the height of the frieze is even, we need to compare the middle two rows

        if friezeHeight%2 == 0:
            lowerRow = friezeHeight//2
            upperRow = lowerRow - 1
            for y in range(friezeLength):
                if self.frieze[upperRow][y][1]: # upperRow cannot pointing southeast
                    return False
                if self.frieze[lowerRow][y][3]: # lowerRow cannot pointing northeast
                    return False
            
            # Then we can flip the lower part to the upper part to make a reflection
            reflection = [[0 for _ in range(friezeLength)] for _ in range(lowerRow)]
            for x in range(lowerRow,friezeHeight):
                for y in range(friezeLength):
                    if self.frieze[x][y][4] and x != lowerRow:
                        reflection[x-lowerRow-1][y] += 1
                    if self.frieze[x][y][3]:
                        reflection[x-lowerRow][y] += 8
                    if self.frieze[x][y][2]:
                        reflection[x-lowerRow][y] += 4
                    if self.frieze[x][y][1]:
                        reflection[x-lowerRow][y] += 2
                if x > lowerRow: # compare the previous reflection row with the original row
                    reflection_rowNum = x - lowerRow - 1
                    frieze_rowNum = friezeHeight - x
                    for i in range(friezeLength):
                        if reflection[reflection_rowNum][i] != self.frieze[frieze_rowNum][i][0]:
                            return False
            # Compare the last reflection row with the original row
            for i in range(friezeLength):
                if reflection[-1][i] != self.frieze[0][i][0]:
                    return False
            return True
        else:
            # If the height of the frieze is odd, we need to check the middle row first
            middleRow = friezeHeight//2
            for i in range(friezeLength):
                if self.frieze[middleRow][i][4]:
                    if not self.frieze[middleRow+1][i][4]: # the next row should also pointing north
                        return False
                if self.frieze[middleRow][i][3]:
                    if not self.frieze[middleRow][i][1]: # the reflection should pointing southeast
                        return False
                if self.frieze[middleRow][i][1]:
                    if not self.frieze[middleRow][i][3]: # the reflection should pointing northeast
                        return False
                if self.frieze[middleRow+1][i][4]:
                    if not self.frieze[middleRow][i][4]: # the reflection should be in the middle row
                        return False

            reflection = [[0 for _ in range(friezeLength)] for _ in range(middleRow)]
            startRow = middleRow+1
            for x in range(startRow, friezeHeight):
                for y in range(friezeLength):
                    if self.frieze[x][y][4] and x != startRow: # xxx1
                        reflection[x-startRow-1][y] += 1
                    if self.frieze[x][y][3]: # xx1x
                        reflection[x-startRow][y] += 8
                    if self.frieze[x][y][2]: # x1xx
                        reflection[x-startRow][y] += 4
                    if self.frieze[x][y][1]: # 1xxx
                        reflection[x-startRow][y] += 2
                if x > startRow:
                    reflection_rowNum = x - startRow - 1
                    frieze_rowNum = friezeHeight - x
                    for i in range(friezeLength):
                        if reflection[reflection_rowNum][i] != self.frieze[frieze_rowNum][i][0]:
                            return False
            for i in range(friezeLength):
                if reflection[-1][i] != self.frieze[0][i][0]:
                    return False
            return True


    def _check_glided_horizontal_reflection(self):
        if self.period % 2 == 1:
            return False
        friezeHeight = len(self.frieze)
        friezeLength = len(self.frieze[0])
        glide_period = self.period // 2

        if friezeHeight % 2 == 0:
            lowerRow = friezeHeight//2
            last_row_num = lowerRow - 1
            
            reflection = [[0 for _ in range(friezeLength)] for _ in range(lowerRow)]
            for x in range(lowerRow):
                for y in range(friezeLength):
                    if self.frieze[x][y][4]:
                        reflection[last_row_num-x+1][y] += 1
                    if self.frieze[x][y][3]:
                        reflection[last_row_num-x][y] += 8
                    if self.frieze[x][y][2]:
                        reflection[last_row_num-x][y] += 4
                    if self.frieze[x][y][1]:
                        reflection[last_row_num-x][y] += 2
            friezeLength -= 1
            for y in range(friezeLength+1):
                if self.frieze[lowerRow][y][4]:
                    reflection[0][y] += 1
                if self.frieze[lowerRow][y][3] and not self.frieze[lowerRow-1][(y+glide_period)%friezeLength][1]:
                    return False
            
            for x in range(lowerRow):
                for y in range(friezeLength):
                    if reflection[x][y] != self.frieze[lowerRow+x][(y+glide_period)%friezeLength][0]:
                        return False
            return True
        else:
            # If the height of the frieze is odd, we need to check the middle row
            middleRow = friezeHeight//2
            
            reflection = [[0 for _ in range(friezeLength)] for _ in range(middleRow+1)]
            # Check whether it is glide reflection on the middle row
            lower_frieze_first_row = [self.frieze[middleRow][y][0] for y in range(friezeLength)]
            for y in range(friezeLength):
                if self.frieze[middleRow][y][4]: # xxx1
                    lower_frieze_first_row[y] -= 1
                if self.frieze[middleRow][y][3]: # xx1x
                    lower_frieze_first_row[y] -= 2
            # compute the reflection of the middle row
            for y in range(friezeLength):
                if self.frieze[middleRow][y][3]: # xx1x
                    reflection[0][y] += 8
                if self.frieze[middleRow][y][2]: # x1xx
                    reflection[0][y] += 4
                if self.frieze[middleRow][y][4]: # xxx1
                    reflection[1][y] += 1 # the height of the frieze is at least equal to 2 which means at least 3 lines so reflection[1][y] is safe

            friezeLength -= 1
            
            for y in range(friezeLength):
                if reflection[0][y] != lower_frieze_first_row[(y+glide_period)%friezeLength]:
                    return False
                    
            for x in range(middleRow):
                for y in range(friezeLength+1):
                    if self.frieze[x][y][4]: # xxx1
                        reflection[middleRow-x+1][y] += 1
                    if self.frieze[x][y][3]: # xx1x
                        reflection[middleRow-x][y] += 8
                    if self.frieze[x][y][2]: # x1xx
                        reflection[middleRow-x][y] += 4
                    if self.frieze[x][y][1]: # 1xxx
                        reflection[middleRow-x][y] += 2

            for x in range(1, middleRow+1):
                for y in range(friezeLength):
                    if reflection[x][y] != self.frieze[middleRow+x][(y+glide_period)%friezeLength][0]:
                        return False
            return True

        
    def _check_rotation_reflection(self):
        friezeLength = len(self.frieze[0]) - 1
        friezeHeigth = len(self.frieze)
        if friezeHeigth%2: # odd
            middle = friezeHeigth//2
            m = friezeHeigth//2
        else:
            middle = friezeHeigth//2-1
            m = friezeHeigth/2-0.5
        for i in range(self.period+1):
            is_rotation_reflection = True
            for x in range(friezeHeigth):
                if not is_rotation_reflection:
                    break
                for y in range(friezeLength):
                    if self.frieze[x][y][4] and not self.frieze[int(2*m-x+1)][(2*i-y)%friezeLength][4]:
                        is_rotation_reflection = False
                        break
                    if self.frieze[x][y][3] and not self.frieze[int(2*m-x+1)][(2*i-y-1)%friezeLength][3]:
                        is_rotation_reflection = False
                        break
                    if self.frieze[x][y][2] and not self.frieze[int(2*m-x)][(2*i-y-1)%friezeLength][2]:
                        is_rotation_reflection = False
                        break
                    if self.frieze[x][y][1] and not self.frieze[int(2*m-x-1)][(2*i-y-1)%friezeLength][1]:
                        is_rotation_reflection = False
                        break
            if is_rotation_reflection:
                return True
        
        for i in range(self.period+1):
            is_rotation_reflection = True
            i_plus = i + 0.5
            for x in range(friezeHeigth):
                if not is_rotation_reflection:
                    break
                for y in range(friezeLength):
                    if self.frieze[x][y][4] and not self.frieze[int(2*m-x+1)][int(2*i_plus-y)%friezeLength][4]:
                        is_rotation_reflection = False
                        break
                    if self.frieze[x][y][3] and not self.frieze[int(2*m-x+1)][int(2*i_plus-y-1)%friezeLength][3]:
                        is_rotation_reflection = False
                        break
                    if self.frieze[x][y][2] and not self.frieze[int(2*m-x)][int(2*i_plus-y-1)%friezeLength][2]:
                        is_rotation_reflection = False
                        break
                    if self.frieze[x][y][1] and not self.frieze[int(2*m-x-1)][int(2*i_plus-y-1)%friezeLength][1]:
                        is_rotation_reflection = False
                        break
            if is_rotation_reflection:
                return True
        return False
                    

    def display(self):
        with open(self.fName[:-4] + '.tex', 'w') as texFile:
            friezeLenght = len(self.frieze[0])
            friezeHeight = len(self.frieze)
            texFile.write("\\documentclass[10pt]{article}\n\\usepackage{tikz}\n\\usepackage[margin=0cm]{geometry}\n\\pagestyle{empty}\n")
            texFile.write("\n")
            texFile.write("\\begin{document}\n")
            texFile.write("\n")
            texFile.write("\\vspace*{\\fill}\n\\begin{center}\n\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]\n")
            texFile.write("% North to South lines\n")
            
            x = 0
            y = 0
            while y < friezeLenght:
                while x < friezeHeight:
                    if self.frieze[x][y][4]:
                        texFile.write(f'    \\draw ({y},{x-1}) -- ')
                        while True:
                            x += 1
                            if x == friezeHeight or not self.frieze[x][y][4]:
                                texFile.write(f'({y},{x-1});\n')
                                break
                    else:
                        x += 1
                x = 0
                y += 1

            texFile.write("% North-West to South-East lines\n")
            
            diagonalSet = set()
            for x in range(friezeHeight):
                for y in range(friezeLenght):
                    if self.frieze[x][y][1] and (x,y) not in diagonalSet:
                        diagonalSet.add((x,y))
                        texFile.write(f'    \\draw ({y},{x}) -- ')
                        xTemp, yTemp = x, y
                        x += 1
                        y += 1
                        while self.frieze[x][y][1]:
                            diagonalSet.add((x,y))
                            x += 1
                            y += 1
                        texFile.write(f'({y},{x});\n')
                        x, y = xTemp, yTemp
            
            texFile.write("% West to East lines\n")
            
            x = 0
            y = 0
            while x < friezeHeight:
                while y < friezeLenght:
                    if self.frieze[x][y][2]:
                        texFile.write(f'    \\draw ({y},{x}) -- ')
                        while self.frieze[x][y][2]:
                            y += 1
                        texFile.write(f'({y},{x});\n')
                    else:
                        y += 1
                y = 0
                x += 1
            
            texFile.write("% South-West to North-East lines\n")
            
            diagonalSet = set()
            southeast_northeast_coordinate = []
            for x in range(friezeHeight):
                for y in range(friezeLenght):
                    if self.frieze[x][y][3] and (x,y) not in diagonalSet:
                        diagonalSet.add((x,y))
                        endPoint = (x-1,y+1)
                        xTemp, yTemp = x, y
                        while True:
                            x += 1
                            y -= 1
                            if x == friezeHeight or y < 0 or not self.frieze[x][y][3]:
                                southeast_northeast_coordinate.append(((x-1,y+1),(endPoint[0],endPoint[1])))
                                break
                            else:
                                diagonalSet.add((x,y))
                        x, y = xTemp, yTemp
            southeast_northeast_coordinate.sort(key = lambda x: x[0]) # Sort the list according to the starting point
            for val in southeast_northeast_coordinate:
                texFile.write(f'    \\draw ({val[0][1]},{val[0][0]}) -- ({val[1][1]},{val[1][0]});\n')

            texFile.write("\\end{tikzpicture}\n\\end{center}\n\\vspace*{\\fill}\n")
            texFile.write("\n")
            texFile.write("\\end{document}\n")


