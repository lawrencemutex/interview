import numpy

class AggregationHandler:
    def __init__(self, dataset):
        self.dataset = dataset

    def aggregate(self):
        """
        aggregates the dataset provided
        """
        attributes = [
            'interest_rate',
            'original_principal_amount', 
            'cancelled_amount', 
            'undisbursed_amount', 
            'disbursed_amount', 
            'repaid_to_ibrd', 
            'due_to_ibrd', 
            'exchange_adjustment', 
            'borrower_obligation', 
            'sold_3rd_party', 
            'repaid_3rd_party', 
            'due_3rd_party', 
            'loans_held'
        ]

        column_aggregations = []
        whisker_chart_data = []
        for attribute in attributes:
            attribute_overview = {
                'attribute': attribute,
                'max': self.dataset[attribute].max(),
                'min': self.dataset[attribute].min(),
                'sum': self.dataset[attribute].sum(),                
                'mean': self.dataset[attribute].mean(),
                'mean_absolute_deviation': self.dataset[attribute].mad(),
                'standard_deviation': self.dataset[attribute].std()
            }
            column_aggregations.append(attribute_overview)

            # getting the quartiles
            record = {
                'label': attribute,
                'y': [
                    self.dataset[attribute].min(),
                    numpy.percentile(self.dataset[attribute], 25),
                    numpy.percentile(self.dataset[attribute], 50),
                    numpy.percentile(self.dataset[attribute], 75),
                    self.dataset[attribute].max(),                    
                ]
            }
            whisker_chart_data.append(record)
              
        summary = {
            'total': len(self.dataset.index),
            "Biggest borrower": "",
            "Most taken loan type": "",
            "aggregations": column_aggregations,
            "whisker": whisker_chart_data
        }
        return summary
        