class DisjointSet:

    # creates a disjoint set from a list
    def __init__(self, startList):

        # make sure there are no duplicate elements
        startList = list(set(startList))

        self.mainList = []

        for element in startList:
            self.mainList.append([element])

    # returns the index of the partition the element is found
    # returns -1 if the element is not found
    def find(self, element):

        count = 0

        for partition in self.mainList:

            if element in partition:
                return count;

            count += 1
        
        return -1;

    # combines the two partitions of element1 and element2 if they aren't already in the same partition
    def combine(self, element1, element2):

        partition1Index = self.find(element1)
        partition2Index = self.find(element2)

        # don't try to combine the same partition to it's self or one that doesn't exist
        if (partition1Index != partition2Index and partition1Index != -1 and partition2Index != -1):

            partition1 = self.mainList[partition1Index]
            partition2 = self.mainList[partition2Index]

            # pick the smaller partition and move it into the larger one
            bigPartition = partition1
            smallPartition = partition2

            if (len(partition2) > len(partition1)):
                bigPartition = partition2
                smallPartition = partition1

            for element in smallPartition:
                bigPartition.append(element)

            # get rid of the emptied partition
            self.mainList.remove(smallPartition)

    def __repr__(self):

        string = "[\n"

        for partition in self.mainList:
            string += "\t" + partition.__repr__() + "\n"

        string += "\n]"

        return string

# test stuff
if __name__ == "__main__":

    testSet = DisjointSet([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    print(testSet)
    print(testSet.find(1))
    testSet.combine(2, 9)
    print(testSet)
    testSet.combine(2, 7)
    print(testSet)
    print(testSet.find(7) == testSet.find(9))
    print(testSet.find(7) == testSet.find(3))